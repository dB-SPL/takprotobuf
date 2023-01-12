#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Greg Albrecht <oss@undef.net>
# Copyright 2020 Delta Bravo-15
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


from datetime import datetime

import re

import untangle

from .constants import DEFAULT_PROTO_HEADER
from .proto import TakMessage


def xml2proto(xml):
    """Convert plain XML CoT to Protobuf."""
    cot = untangle.parse(xml)
    tak_message = TakMessage()
    tak_control = tak_message.takControl
    cot_event = tak_message.cotEvent


    event = cot.event
    if not event:
        return None

    # If this is a GeoChat message, extract the sender's UID from the event UID and
    # place it in takControl.contactUid
    uid = event.get("uid")
    if uid and "GeoChat." in uid:
        tak_control.contactUid = uid.split(".")[1]

    base_attribs = ['type', 'access', 'qos', 'opex', 'uid', 'how']

    for attrib in base_attribs:
        val = event.get(attrib)
        if val:
            setattr(cot_event, attrib, val)

    # TAK protobuf times are expressed as miliseconds since 1970-01-01 00:00:00 UTC
    # Convert time, start, and stale, from ISO time format to miliseconds since epoch
    if cot.event['time']:
        send_time = datetime.strptime(cot.event['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        send_time = int(send_time.timestamp() * 1000)
        cot_event.sendTime = send_time
            
    if cot.event['start']:
        start_time = datetime.strptime(cot.event['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
        start_time = int(start_time.timestamp() * 1000)
        cot_event.startTime = start_time

    if cot.event['stale']:
        stale_time = datetime.strptime(cot.event['stale'], '%Y-%m-%dT%H:%M:%S.%fZ')
        stale_time = int(stale_time.timestamp() * 1000)
        cot_event.staleTime = stale_time

    # If the event element includes a point child, write the attributes
    point = event.get("point")
    if point:
        attribs = ['lat', 'lon', 'hae', 'ce', 'le']
        for attrib in attribs:
            val = point.get(attrib)
            if val:
                setattr(cot_event, attrib, float(val))

    detail = event.get("detail")
    if detail:
        # If the XML includes a <detail> element, create cot_event.detail
        new_detail = cot_event.detail

        # The cot_event.detail field of a TAK protobuf is structured differently
        # from CoT XML. cot_event.detail may only contain xmlDetail, contact,
        # __group, precisionlocation, status, takv, and track. xmlDetail should
        # contain an XML string with any data that does not adhere to the other
        # strongly-typed fields. See more information about each field below.

        # If this is a GeoChat message, write the contents of <detail> in xmlDetail.
        if uid and "GeoChat." in uid:
            pattern = "<detail>(.*?)</detail>"
            xmldetailstr = re.search(pattern, xml).group(1)
            new_detail.xmlDetail = xmldetailstr

        contact = detail.get("contact")
        if contact:
            attribs = ["endpoint", "callsign"]
            for attrib in attribs:
                attrib_val = contact.get(attrib)
                if attrib_val:
                    setattr(new_detail, attrib, attrib_val)

        group = detail.get("__group")  # pylint: disable=protected-access
        if group:
            attribs = ["name", "role"]
            for attrib in attribs:
                attrib_val = group.get(attrib)
                if attrib_val:
                    setattr(new_detail.group, attrib, attrib_val)

        prec_loc = detail.get("precisionlocation")
        if prec_loc:
            attribs = ["geopointsrc", "altsrc"]
            for attrib in attribs:
                attrib_val = prec_loc.get(attrib)
                if attrib_val:
                    setattr(new_detail.precisionLocation, attrib, attrib_val)

        status = detail.get("status")
        if status:
            battery = status.get("battery")
            if battery:
                new_detail.status.battery = int(battery)

        takv = detail.get("takv")
        if takv:
            attribs = ["device", "platform", "os", "version"]
            for attrib in attribs:
                attrib_val = takv.get(attrib)
                if attrib_val:
                    setattr(new_detail.takv, attrib, attrib_val)

        # The fields in track are double-precision floating-point numbers.
        # We can use Python's native float, since that is actually 64-bit
        # floating-point.
        track = detail.get("track")
        if track:
            attribs = ["speed", "course"]
            for attrib in attribs:
                attrib_val = track.get(attrib)
                if attrib_val:
                    setattr(new_detail.track, attrib, float(attrib_val))

    # TAK protocol packets have a three-byte header.  The two 0xbf bytes on the outside
    # identify the packet as containing TAK protocol.  The 0x01 byte in the middle
    # identifies the TAK protocol version, in our case, version 1.
    header_bytearray = DEFAULT_PROTO_HEADER
    takmessage_bytearray = bytearray(tak_message.SerializeToString())
    output_bytearray = header_bytearray + takmessage_bytearray

    return output_bytearray

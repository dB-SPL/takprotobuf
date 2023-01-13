#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Greg Albrecht <oss@undef.net>
# Copyright 2020 Delta Bravo-15 <deltabravo15ga@gmail.com>
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

import xml.etree.ElementTree as ET

from .proto import TakMessage


DEFAULT_PROTO_HEADER = bytearray(b"\xbf\x01\xbf")
ISO_8601_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_proto(binary):
    """Parse CoT message."""
    header = binary[:3]
    if header != DEFAULT_PROTO_HEADER:
        return None

    binary = binary[3:]
    protobuf = TakMessage()
    protobuf.ParseFromString(binary)

    return protobuf


def format_time(time) -> int:
    """Format timestamp as microseconds."""
    s_time = datetime.strptime(time + "+0000", ISO_8601_UTC + "%z")
    return int(s_time.timestamp() * 1000)


def xml2proto(xml):
    """Convert plain XML CoT to Protobuf."""
    event = ET.fromstring(xml)
    tak_message = TakMessage()
    tak_control = tak_message.takControl
    new_event = tak_message.cotEvent

    # If this is a GeoChat message, extract the sender's UID from the event UID and
    # place it in takControl.contactUid
    uid = event.get("uid")
    if uid and "GeoChat." in uid:
        tak_control.contactUid = uid.split(".")[1]

    base_attribs = ["type", "access", "qos", "opex", "uid", "how"]
    for attrib in base_attribs:
        val = event.get(attrib)
        if val:
            setattr(new_event, attrib, val)

    # TAK protobuf times are expressed as miliseconds since 1970-01-01 00:00:00 UTC
    # Convert time, start, and stale, from ISO time format to miliseconds since epoch
    time_attribs = ["time", "start", "stale"]
    for attrib in time_attribs:
        val = event.get(attrib)
        if val:
            if attrib == "time":
                attrib = "send"
            setattr(new_event, f"{attrib}Time", format_time(val))

    # If the event element includes a point child, write the attributes
    point = event.find("point")
    if point is not None:
        attribs = ['lat', 'lon', 'hae', 'ce', 'le']
        for attrib in attribs:
            val = point.get(attrib)
            if val:
                setattr(new_event, attrib, float(val))

    detail = event.find("detail")
    if detail is not None:
        # If the XML includes a <detail> element, create new_event.detail
        new_detail = new_event.detail

        # The new_event.detail field of a TAK protobuf is structured differently
        # from CoT XML. new_event.detail may only contain xmlDetail, contact,
        # __group, precisionlocation, status, takv, and track. xmlDetail should
        # contain an XML string with any data that does not adhere to the other
        # strongly-typed fields. See more information about each field below.

        # If this is a GeoChat message, write the contents of <detail> in xmlDetail.
        if uid and "GeoChat." in uid:
            pattern = "<detail>(.*?)</detail>"
            xmldetailstr = re.search(pattern, xml).group(1)
            new_detail.xmlDetail = xmldetailstr
        else:
            # Add unknown elements to xmlDetail field.
            known_elem = [
                "contact", "__group", "precisionlocation", "status", "takv", "track"]
            for elem in detail.iterfind("*"):
                if elem.tag not in known_elem:
                    new_detail.xmlDetail = ET.tostring(elem)

        contact = detail.find("contact")
        if contact is not None:
            attribs = ["endpoint", "callsign"]
            for attrib in attribs:
                attrib_val = contact.get(attrib)
                if attrib_val:
                    setattr(new_detail.contact, attrib, attrib_val)

        group = detail.find("__group")  # pylint: disable=protected-access
        if group is not None:
            attribs = ["name", "role"]
            for attrib in attribs:
                attrib_val = group.get(attrib)
                if attrib_val:
                    setattr(new_detail.group, attrib, attrib_val)

        prec_loc = detail.find("precisionlocation")
        if prec_loc is not None:
            attribs = ["geopointsrc", "altsrc"]
            for attrib in attribs:
                attrib_val = prec_loc.get(attrib)
                if attrib_val:
                    setattr(new_detail.precisionLocation, attrib, attrib_val)

        status = detail.find("status")
        if status is not None:
            battery = status.get("battery")
            if battery:
                new_detail.status.battery = int(battery)

        takv = detail.find("takv")
        if takv is not None:
            attribs = ["device", "platform", "os", "version"]
            for attrib in attribs:
                attrib_val = takv.get(attrib)
                if attrib_val:
                    setattr(new_detail.takv, attrib, attrib_val)

        # The fields in track are double-precision floating-point numbers.
        # We can use Python's native float, since that is actually 64-bit
        # floating-point.
        track = detail.find("track")
        if track is not None:
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

import untangle
import time
from datetime import datetime
import re
from .proto import TakMessage

def xmlToProto(xml):
	cot = untangle.parse(xml)
	takMessage = TakMessage()
	takControl = takMessage.takControl
	cotEvent = takMessage.cotEvent

	# If this is a GeoChat message, extract the sender's UID from the event UID and place it in takControl.contactUid
	if "GeoChat." in cot.event['uid']:
		takControl.contactUid = cot.event['uid'].split(".")[1]

	# If XML contains an event element, write the attributes
	if 'event' in dir(cot):		
		if cot.event['type']:
			cotEvent.type = cot.event['type']

		if cot.event['access']:
			cotEvent.access = cot.event['access']

		if cot.event['qos']:
			cotEvent.qos = cot.event['qos']

		if cot.event['opex']:
			cotEvent.opex = cot.event['opex']

		if cot.event['uid']:
			cotEvent.uid = cot.event['uid']

		# TAK protobuf times are expressed as miliseconds since 1970-01-01 00:00:00 UTC
		# Convert time, start, and stale, from ISO time format to miliseconds since epoch
		if cot.event['time']:
			sendTime = datetime.strptime(cot.event['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
			sendTime = int(sendTime.timestamp() * 1000)
			cotEvent.sendTime = sendTime
					
		if cot.event['start']:
			startTime = datetime.strptime(cot.event['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
			startTime = int(startTime.timestamp() * 1000)
			cotEvent.startTime = startTime

		if cot.event['stale']:
			staleTime = datetime.strptime(cot.event['stale'], '%Y-%m-%dT%H:%M:%S.%fZ')
			staleTime = int(staleTime.timestamp() * 1000)
			cotEvent.staleTime = staleTime

		if cot.event['how']:
			cotEvent.how = cot.event['how']

		# If the event element includes a point child, write the attributes
		if 'point' in dir(cot.event):

			if cot.event.point['lat']:
				cotEvent.lat = float(cot.event.point['lat'])

			if cot.event.point['lon']:
				cotEvent.lon = float(cot.event.point['lon'])

			if cot.event.point['hae']:
				cotEvent.hae = float(cot.event.point['hae'])

			if cot.event.point['ce']:
				cotEvent.ce = float(cot.event.point['ce'])

			if cot.event.point['le']:
				cotEvent.le = float(cot.event.point['le'])

		# If the XML includes a <detail> element, create cotEvent.detail
		if 'detail' in dir(cot.event):
			detail = cotEvent.detail
			
			# The cotEvent.detail field of a TAK protobuf is structured differently from CoT XML.
			# cotEvent.detail may only contain xmlDetail, contact, __group, precisionlocation, status,
			# takv, and track. xmlDetail should contain an XML string with any data that does not
			# adhere to the other strongly-typed fields. See more information about each field below.
			
			# If this is a GeoChat message, write the contents of <detail> in xmlDetail.
			if "GeoChat." in cot.event['uid']:
				pattern = "<detail>(.*?)</detail>"
				xmldetailstr = re.search(pattern, xml).group(1)
				detail.xmlDetail = xmldetailstr

			if 'contact' in dir(cot.event.detail):
				if cot.event.detail.contact['endpoint']:
					detail.contact.endpoint = cot.event.detail.contact['endpoint'] # must be a string

				if cot.event.detail.contact['callsign']:
					detail.contact.callsign = cot.event.detail.contact['callsign'] # must be a string

				if '__group' in dir(cot.event.detail):
					if cot.event.detail.__group['name']:
						detail.group.name = cot.event.detail.__group['name'] # must be a string

					if cot.event.detail.__group['role']:
						detail.group.role = cot.event.detail.__group['role'] # must be a string

					if 'precisionlocation' in dir(cot.event.detail):
						if cot.event.detail.precisionlocation['geopointsrc']:
							detail.precisionLocation.geopointsrc = cot.event.detail.precisionlocation['geopointsrc'] # must be a string
							
						if cot.event.detail.precisionlocation['altsrc']:
							detail.precisionLocation.altsrc = cot.event.detail.precisionlocation['altsrc'] # must be a string

			if 'status' in dir(cot.event.detail):
				if cot.event.detail.status['battery']:
					detail.status.battery = int(cot.event.detail.status['battery']) # must be an integer

			if 'takv' in dir(cot.event.detail):
				if cot.event.detail.takv['device']:
					detail.takv.device = cot.event.detail.takv['device'] # must be a string

				if cot.event.detail.takv['platform']:
					detail.takv.platform = cot.event.detail.takv['platform'] # must be a string

				if cot.event.detail.takv['os']:
					detail.takv.os = cot.event.detail.takv['os'] # must be a string

				if cot.event.detail.takv['version']:
					detail.takv.version = cot.event.detail.takv['version'] # must be a string

			# The fields in track are double-precision floating-point numbers.
			# We can use Python's native float, since that is actually 64-bit floating-point.
			if 'track' in dir(cot.event.detail):
				if cot.event.detail.track['speed']:
					detail.track.speed = float(cot.event.detail.track['speed']) # must be floating-point

				if cot.event.detail.track['course']:
					detail.track.course = float(cot.event.detail.track['course']) # must be floating-point
					
	
	# TAK protocol packets have a three-byte header.  The two 0xbf bytes on the outside identify the packet
	# as containing TAK protocol.  The 0x01 byte in the middle identifies the TAK protocol version, in our
	# case, version 1.
	headerByteArray = bytearray(b'\xbf\x01\xbf')
	takMessageByteArray = bytearray(takMessage.SerializeToString())
	outputByteArray = headerByteArray + takMessageByteArray
	return outputByteArray
import untangle
import time
from datetime import datetime
import sys
import re
from .proto import TakMessage

# Read XML from STDIN and parse
#str = sys.stdin.read()

# Read XML from local file
#with open('chat.xml', 'r') as file:
#	xml = file.read()
#	file.close()

def renderProto(xml):
	cot = untangle.parse(xml)
	takMessage = TakMessage()
	takControl = takMessage.takControl
	cotEvent = takMessage.cotEvent

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

		# If the XML includes a Detail element, write the attributes
		if 'detail' in dir(cot.event):
			detail = cotEvent.detail
			if "GeoChat." in cot.event['uid']:
				pattern = "<detail>(.*?)</detail>"
				xmldetailstr = re.search(pattern, xml).group(1)
				detail.xmlDetail = xmldetailstr

			if 'contact' in dir(cot.event.detail):
				if cot.event.detail.contact['endpoint']:
					detail.contact.endpoint = cot.event.detail.contact['endpoint']

				if cot.event.detail.contact['callsign']:
					detail.contact.callsign = cot.event.detail.contact['callsign']

				if '__group' in dir(cot.event.detail):
					if cot.event.detail.__group['name']:
						detail.group.name = cot.event.detail.__group['name']

					if cot.event.detail.__group['role']:
						detail.group.role = cot.event.detail.__group['role']

					if 'precisionlocation' in dir(cot.event.detail):
						if cot.event.detail.precisionlocation['geopointsrc']:
							detail.precisionlocation.geopointsrc = cot.detail.precisionlocation['geopointsrc']
							if cot.event.detail.precisionlocation['altsrc']:
								detail.precisionlocation.altsrc = cot.detail.precisionlocation['altsrc']

			if 'status' in dir(cot.event.detail):
				if cot.event.detail.status['battery']:
					detail.status.battery = int(cot.event.detail.status['battery'])

			if 'takv' in dir(cot.event.detail):
				if cot.event.detail.takv['device']:
					detail.takv.device = cot.event.detail.takv['device']

				if cot.event.detail.takv['platform']:
					detail.takv.platform = cot.event.detail.takv['platform']

				if cot.event.detail.takv['os']:
					detail.takv.os = cot.event.detail.takv['os']

				if cot.event.detail.takv['version']:
					detail.takv.version = cot.event.detail.takv['version']

			if 'track' in dir(cot.event.detail):
				if cot.event.detail.track['speed']:
					detail.track.speed = float(cot.event.detail.track['speed'])

				if cot.event.detail.track['course']:
					detail.track.course = float(cot.event.detail.track['course'])
					
	headerByteArray = bytearray(b'\xbf\x01\xbf')
	takMessageByteArray = bytearray(takMessage.SerializeToString())
	outputByteArray = headerByteArray + takMessageByteArray
	return outputByteArray
	
def parseProto(binary):
	binary = binary[3:]
	protobuf = TakMessage()
	protobuf.ParseFromString(binary)
	return protobuf
	

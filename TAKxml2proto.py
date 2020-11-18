import os
import untangle
import time
from datetime import datetime
import sys
import re

# Read XML from STDIN and parse
xml = sys.stdin.read()

cot = untangle.parse(xml)

# Clear contents of output file
outtxt = open('out.txt', 'w')
outtxt.close()
# Open output file for writing
outtxt = open("out.txt", "a")
# include blank takControl element - need to add parsing for takControl elements in GeoChat messages
outtxt.write("takControl {\n")
if "GeoChat" in cot.event['uid']:
	contactUid = cot.event['uid'].split(".")[1]
	outtxt.write("  contactUid: \"" + contactUid + "\"\n")
outtxt.write("}\n")

# If XML contains an event element, write the attributes
if 'event' in dir(cot):
	outtxt.write("cotEvent {\n")
	if cot.event['type']:
		outtxt.write("  type: \"" + cot.event['type'] + "\"\n")
		epoch = datetime.utcfromtimestamp(0)
	
	if cot.event['access']:
		outtxt.write("  access: \"" + cot.event['access'] + "\"\n")
		
	if cot.event['qos']:
		outtxt.write("  qos: \"" + cot.event['qos'] + "\"\n")
		
	if cot.event['opex']:
		outtxt.write("  opex: \"" + cot.event['opex'] + "\"\n")
	
	if cot.event['uid']:
		outtxt.write("  uid: \"" + cot.event['uid'] + "\"\n")
		
	if cot.event['time']:
		sendTime = datetime.strptime(cot.event['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
		sendTime = str(int(sendTime.timestamp() * 1000))
		outtxt.write("  sendTime: " + sendTime + "\n")
		
	if cot.event['start']:
		startTime = datetime.strptime(cot.event['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
		startTime = str(int(startTime.timestamp() * 1000))
		outtxt.write("  startTime: " + startTime + "\n")
		
	if cot.event['stale']:
		staleTime = datetime.strptime(cot.event['stale'], '%Y-%m-%dT%H:%M:%S.%fZ')
		staleTime = str(int(staleTime.timestamp() * 1000))
		outtxt.write("  staleTime: " + staleTime + "\n")
		
	if cot.event['how']:
		outtxt.write("  how: \"" + cot.event['how'] + "\"\n")
		
	# If the event element includes a point child, write the attributes
	if 'point' in dir(cot.event):
		if cot.event.point['lat']:
			outtxt.write("  lat: " + cot.event.point['lat'] + "\n")
		
		if cot.event.point['lon']:
			outtxt.write("  lon: " + cot.event.point['lon'] + "\n")
			
		if cot.event.point['hae']:
			outtxt.write("  hae: " + cot.event.point['hae'] + "\n")
			
		if cot.event.point['ce']:
			outtxt.write("  ce: " + cot.event.point['ce'] + "\n")
			
		if cot.event.point['le']:
			outtxt.write("  le: " + cot.event.point['le'] + "\n")
			
			# If the XML includes a Detail element, write the attributes
			if 'detail' in dir(cot.event):
				outtxt.write("  detail {\n")
				
				if "GeoChat." in cot.event['uid']:
					pattern = "<detail>(.*?)</detail>"
					xmldetailstr = re.search(pattern, xml).group(1)
					xmldetailstr = xmldetailstr.replace("\'", "\\\'").replace("\"", "\\\"")
					outtxt.write("    xmlDetail: \"" + xmldetailstr + "\"\n")
					
				if 'contact' in dir(cot.event.detail):
					outtxt.write("    contact {\n")
						
					if cot.event.detail.contact['endpoint']:
						outtxt.write("      endpoint: \"" + cot.event.detail.contact['endpoint'] + "\"\n")
							
					if cot.event.detail.contact['callsign']:
						outtxt.write("      callsign: \"" + cot.event.detail.contact['callsign'] + "\"\n")
												
					outtxt.write("    }\n")
						
				if '__group' in dir(cot.event.detail):
					outtxt.write("    group {\n")
					if cot.event.detail.__group['name']:
						outtxt.write("      name: \"" + cot.event.detail.__group['name'] + "\"\n")
								
					if cot.event.detail.__group['role']:
						outtxt.write("      role: \"" + cot.event.detail.__group['role'] + "\"\n")
						
					outtxt.write("    }\n")
						
				if 'precisionlocation' in dir(cot.event.detail):
					outtxt.write("    precisionlocation {\n")
					if cot.event.detail.precisionlocation['geopointsrc']:
						outtxt.write("      geopointsrc: \"" + cot.detail.precisionlocation['geopointsrc'] + "\"\n")
							
					if cot.event.detail.precisionlocation['altsrc']:
						outtxt.write("      altscr: \"" + cot.detail.precisionlocation['altsrc'] + "\"\n")
							
					outtxt.write("    }\n")
						
				if 'status' in dir(cot.event.detail):
					outtxt.write("    status {\n")
					if cot.event.detail.status['battery']:
						outtxt.write("      battery: " + cot.event.detail.status['battery'] + "\n")
							
					outtxt.write("    }\n")
				if 'takv' in dir(cot.event.detail):
					outtxt.write("    takv {\n")
					if cot.event.detail.takv['device']:
						outtxt.write("      device : \"" + cot.event.detail.takv['device'] + "\"\n")
						
					if cot.event.detail.takv['platform']:
						outtxt.write("      platform : \"" + cot.event.detail.takv['platform'] + "\"\n")
						
					if cot.event.detail.takv['os']:
						outtxt.write("      os: \"" + cot.event.detail.takv['os'] + "\"\n")
						
					if cot.event.detail.takv['version']:
						outtxt.write("      version: \"" + cot.event.detail.takv['version'] + "\"\n")
						
						outtxt.write("    }\n")

					if cot.event.detail.track._name:
						outtxt.write("    track {\n")
						if cot.event.detail.track['speed']:
							outtxt.write("      speed: " +  cot.event.detail.track['speed'] + "\n")
							
						if cot.event.detail.track['course']:
							outtxt.write("      course: " + cot.event.detail.track['course'] + "\n")


						outtxt.write("    }\n")

		outtxt.write("  }\n")
	
	outtxt.write("}")

outtxt.close()
outtxt = open('out.txt', 'r')
print(outtxt.read())
outtxt.close()
os.remove('out.txt')


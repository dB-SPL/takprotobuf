from .proto import TakMessage

def parseProto(binary, raw=None):
	header = binary[:3]
	if header != bytearray(b'\xbf\x01\xbf'):
		return -1
	
	else:
		binary = binary[3:]
		protobuf = TakMessage()
		protobuf.ParseFromString(binary)
		return protobuf
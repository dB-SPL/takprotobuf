# takprotobuf

Python library to encode and decode Cursor-on-Target (CoT) messages using Protocol Buffers.

## Usage

The library containst two basic functions, with a thrid in the works.   `parseProto()` decodes a protobuf and returns the contents of the message.  `xmlToProto()` encodes XML to TAK protobuf.  I'll be adding another to encode directly from a Python object or class.

### xmlToProto()

Given a string which contains either a CoT message in XML or the path to an XML file containing a CoT message, the function `xmlToProto(xml)` will return a byte array containing the binary protobuf.

For example, if the string `xml` contained:
```
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/></detail></event>
```
The function would return:
```
from takprotobuf import xmlToProto
xmlToProto(xml)

bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')
```

### parseProto()

Given a bytearray containing a TAK protobuf, `parseProto(binary)` will return an instance of the protobuf class.  You can then access the contents as an object.

If `binary` contains the same bytearray above, the function will return:
```
from takprotobuf import parseProto
decoded = parseProto(binary)
print(decoded)

cotEvent {
  type: "a-f-G-E-V-C"
  uid: "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261"
  sendTime: 1581203444000
  startTime: 1581203444000
  staleTime: 1581203471000
  how: "h-e"
  lat: 43.97957317
  lon: -66.07737696
  hae: 26.767999
  ce: 9999999.0
  le: 9999999.0
  detail {
    contact {
      endpoint: "192.168.1.10:4242:tcp"
      callsign: "Eliopoli HQ"
    }
    group {
      name: "Yellow"
      role: "HQ"
    }
    status {
      battery: 100
    }
    takv {
      device: "LENOVO 20QV0007US"
      platform: "WinTAK-CIV"
      os: "Microsoft Windows 10 Home"
      version: "1.10.0.137"
    }
    track {
    }
  }
}
```

### TAK Protobuf Header Bytes

When TAK clients send UDP packets containing protobufs, there is a three byte header consisting of `0xbf 0x01 0xbf`.  The `xmlToProto()` function adds the header bytes for you, and the `parseProto()` functions expects them to be included in its input.  This may change in the future, as I learn more about the TAK ecosystem.

## To Do

- Clean up processing for the `xmlDetail` element
- Encode protobuf directly from Python object or class
- Exception handling

## Credits

I couldn't have created this without all of the examples of CoT XML provided by the developers of FreeTAKServer at https://github.com/FreeTAKTeam/FreeTakServer/tree/master/docs/Example%20metrics/cot

Built using Protoc, the protobuf compiler https://github.com/protocolbuffers/protobuf

and the .proto files from the ATAK repository https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV/tree/master/commoncommo/core/impl/protobuf

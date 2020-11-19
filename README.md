# takprotobuf

Python script for processing CoT XML for encoding as Protocol Buffers

## Usage

Where the string `xml` contains either a CoT message in XML or the path to an XML file containing a CoT message, the function `renderProto(xml)` will return a byte array containing the binary protobuf.

```
from takprotobuf.TAKxml2protobuf import renderProto
renderProto(xml)
```

For example, if the string `xml` contained:
```
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/></detail></event>
```
The function would return:
```
from takprotobuf.TAKxml2protobuf import renderProto
renderProto(xml)

bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')```
```

## To Do

- Clean up processing for the `xmlDetail` element
- Parse bytearray containing protobuf into Python object
- Exception handling

## Credits

I've included the .proto files required to encode TAK protobufs from the ATAK repository at https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV

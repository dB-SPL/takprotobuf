# TAKxml2protobuf

Python script for processing CoT XML for encoding as Protocol Buffers

## Usage

The script accepts Cursor-on-Target XML messages from STDIN.
It returns a formatted string on the STDOUT ready to be encoded as a protobuf using protoc and the .proto files from the ATAK repo.

```bash
cat input.xml | python3 TAKxml2protobuf.py | protoc --encode TakMessage takmessage.proto > tmp.bin &&
printf "\xbf\x01\xbf" | cat - tmp.bin > output.bin && rm tmp.bin
```
Remember that, before sending the protobuf to a TAK client, you need to add a header consisting of the three bytes "0xbf 0x01 0xbf" to the beginning of the packet.

Currently works well for SA and PLI messages, but the "TakControl" and "detail" elements require more work to be reliable with other types of CoT such as GeoChat messages.

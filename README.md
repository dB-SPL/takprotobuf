# TAKxml2protobuf

Python script for processing CoT XML for encoding as Protocol Buffers

## Usage

The script accepts Cursor-on-Target XML messages from STDIN.
It returns a formatted string on the STDOUT ready to be encoded as a protobuf using protoc and the .proto files from the ATAK repo.


`cat input.xml | python3 TAKxml2protobuf.py`

## To Do

- Properly handle child elements of `<detail>`. In the output, `xmlDetail` should contain a string with plain XML for any elements that are not included in the strongly typed messages included in the TAK .proto files.
- Exception handling

## Credits

I've included the .proto files required to encode TAK protobufs from the ATAK repository at https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV

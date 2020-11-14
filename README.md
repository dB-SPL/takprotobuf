# TAKxml2protobuf

Python script for processing CoT XML for encoding as Protocol Buffers

## Usage

The script accepts Cursor-on-Target XML messages from STDIN.
It returns a formatted string on the STDOUT ready to be encoded as a protobuf using protoc and the .proto files from the ATAK repo.

Currently works well for SA and PLI messages, but the "TakControl" and "detail" elements require more work to be reliable with other types of CoT such as GeoChat messages.

import sys, struct, socket, select, random

packer = struct.Struct("8s")
clt_address = ("localhost", 3000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(clt_address)
    packed_data = packer.pack("Hello".encode())
    client.send(packed_data)

    data = client.recv(8)
    unpacked_data = packer.unpack(data)
    message = unpacked_data[0].decode('utf-8').strip()
    print(f"I got this from the server: {message}")
import sys, struct, socket, select, random

packer = struct.Struct("10s 6s 20s")
clt_address = ("oktnb147.inf.elte.hu", 11224)
msg_to_srv = ("TCPKliens".encode(),"fvmi7v".encode(), "hz5fr570pq6g14l7".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(clt_address)
    packed_data = packer.pack(*msg_to_srv)
    client.send(packed_data)

    packer = struct.Struct("10s 100s")
    data = client.recv(1024)
    unpacked_data = packer.unpack(data)
    message = unpacked_data[1].decode('utf-8').strip()

    packer2 = struct.Struct("3s")
    
    message = (message[5] + message[6] + message[7]).encode()
    packed_data = packer2.pack(message)
    client.send(packed_data)

    data = client.recv(1024)
    unpacked_data = packer.unpack(data)
    message = unpacked_data[1].decode('utf-8').strip()

    print(f"I got this from the server: {message}")
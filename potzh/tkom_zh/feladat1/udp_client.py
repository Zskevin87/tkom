import sys, struct, socket, select, random

packer = struct.Struct("10s 6s 20s")
clt_address = ("oktnb147.inf.elte.hu", 11235)
msg_to_srv = ("UDPKliens".encode(),"fvmi7v".encode(), "ix64f4w0tp7nxrw9".encode())

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    packed_data = packer.pack(*msg_to_srv)
    client.sendto(packed_data, clt_address)

    data, address = client.recvfrom(1024)
    packer = struct.Struct("10s 100s")
    unpacked_data = packer.unpack(data)
    message = unpacked_data[1].decode('utf-8').strip()

    packer2 = struct.Struct("3s")
    
    message = (message[4] + message[7] + message[9]).encode()
    packed_data = packer2.pack(message)
    client.sendto(packed_data, clt_address)

    data, address = client.recvfrom(1024)
    unpacked_data = packer.unpack(data)
    message = unpacked_data[1].decode('utf-8').strip()
    print(f"I got this from the server: {message}")
    
    
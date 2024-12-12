import socket, struct

packer = struct.Struct("10s 6s 20s")
unpacker = struct.Struct("10s 100s")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # addr = ("oktnb147.inf.elte.hu", 11235)
    # sock.connect(addr)
    dataToSend = packer.pack("UDPKliens".encode(),"fvmi7v".encode(), "ix64f4w0tp7nxrw9".encode())
    # sock.send(dataToSend)
    # data = sock.recv(200)
    unpacked_data = unpacker.unpack(data)
    print(unpacked_data)
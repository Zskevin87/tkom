import sys, struct, socket, select, random

packer = struct.Struct("8s")
srv_address = ("localhost", 3000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    try:
        server.bind(srv_address)
        print("Listening for new connection...")
        data, address= server.recvfrom(1024)
        unpacked_data = packer.unpack(data)
        message = unpacked_data[0].decode('utf-8').strip()
        print(f"I got this from the client: {message}")
        print(f"I'm sending something back: Hi!")
        packed_data = packer.pack("Hi!".encode())
        server.sendto(packed_data, address)
    except KeyboardInterrupt:
        print("Closing the server...")
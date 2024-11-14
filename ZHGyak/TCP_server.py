import sys, struct, socket, select, random

packer = struct.Struct("8s")
srv_address = ("localhost", 3000)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    try:
        server.bind(srv_address)
        server.listen(4)
        print("Listening for new connection...")
        client_socket, client_address = server.accept()
        print("Client connected.")
        data = client_socket.recv(packer.size)
        unpacked_data = packer.unpack(data)
        message = unpacked_data[0].decode('utf-8').strip()
        print(f"I got this from the client: {message}")
        print(f"I'm sending something back: Hi!")
        packed_data = packer.pack("Hi!".encode())
        client_socket.send(packed_data)
    except KeyboardInterrupt:
        print("Closing the server...")
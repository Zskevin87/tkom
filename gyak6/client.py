import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    addr = ("127.0.0.1", 9000)
    sock.connect(addr)
    sock.send("Hello".encode())
    print("Hello message sent.")
    data = sock.recv(16)
    print(data.decode())
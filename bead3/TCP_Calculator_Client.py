import socket
import struct

server_addr = ('127.0.0.1', 8000)
packer = struct.Struct('iic')
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        a = input("Give me a number: ")
        b = input("Give me an operator: ")
        c = input("Give me a number: ")
        
        if len(b) > 1:
            print("Operator should be only 1 character!")
            exit(1)

        if b not in "+-*/%":
            print(f"This is not an operator: {b}")
            exit(1)

        packed_data = packer.pack(int(a), int(c), b.encode())
        client.connect(server_addr)
        
        client.send(packed_data)
        data = client.recv(200)
        print("Result: ", data.decode())
    except ValueError:
        print("Please use numbers!")
    except KeyboardInterrupt:
        print("\nInterrupted")
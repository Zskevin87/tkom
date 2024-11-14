import socket
import select
import struct

packer = struct.Struct('iic')
server_addr = ('127.0.0.1', 8000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    print("Listening for new connections...")

    inputs = [server]
    timeout = 1
    
    try:
        while True:
            readable, writeable, exceptional = select.select(inputs, inputs, inputs, timeout)
            
            if not (readable or writeable or exceptional):
                continue
            
            for sock in readable:
                if sock is server: # new connection
                    client, client_addr = sock.accept()
                    inputs.append(client)
                    print("Connected: ", client_addr)
                else: # an existing connection is readable
                    data = sock.recv(packer.size)
                    if not data:
                        print("Logout: ", sock)
                        inputs.remove(sock)
                        sock.close()
                    else:
                        a, b, c = packer.unpack(data)
                        res = eval(str(a) + c.decode() + str(b))
                        sock.send(str(res).encode())
    except KeyboardInterrupt:
        print("Closing the server...")
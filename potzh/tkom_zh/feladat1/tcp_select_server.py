import sys, struct, socket, select, random

packer = struct.Struct("20si?")
srv_address = ("localhost", 12000)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(srv_address)
    server.listen(4)
    print("Listening for new connection...")
    inputs = [server]
    timeout = 10

    try:
        while True:
            readable, writeable, exceptional = select.select(inputs, inputs, inputs, timeout)

            if not (readable or writeable or exceptional):
                print("Data is not Readable/Writeable or the waiting time reached the time out...")
                exit(-1)

            for sock in readable:
                if sock is server: # new connection
                    client, client_addr = sock.accept()
                    inputs.append(client)
                    print("Connected: ", client_addr)

                else:
                    data = sock.recv(packer.size)
                    if not data:
                        print("Logout: ", sock)
                        inputs.remove(sock)
                        sock.close()

                    else:
                        unpacked_data = packer.unpack(data)
                        message = unpacked_data[0].decode('utf-8').strip()
                        print(unpacked_data)
                        messageNum = unpacked_data[1]
                        messageBool = unpacked_data[2]

                        print(message)

                        if(messageBool):
                            msg_to_client = message[:messageNum]
                            print(message)
                            print(msg_to_client)
                        else:
                            msg_to_client = message[-messageNum:]
                            print(message)
                            print(msg_to_client)

                        packer2 = struct.Struct("10s")
                        packed_data = packer2.pack(msg_to_client.encode())
                        sock.send(packed_data)

    except KeyboardInterrupt:
        print("Closing the server...")
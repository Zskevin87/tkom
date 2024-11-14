import socket
import select

proxy_addr = ('localhost', 9000)
people_inf_elte_hu_addr = ('people.inf.elte.hu', 80)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
    proxy.bind(proxy_addr)
    proxy.listen(1)
    print("Listening for new connections...")

    inputs = [proxy]
    timeout = 1
    
    try:
        while True:
            readable, writeable, exceptional = select.select(inputs, inputs, inputs, timeout)
            
            if not (readable or writeable or exceptional):
                continue
            
            for sock in readable:
                if sock is proxy: # new connection
                    client, client_addr = sock.accept()
                    inputs.append(client)
                    print("Connected: ", client_addr)
                else: # an existing connection is readable
                    data = sock.recv(65000)
                    if not data:
                        print("Logout: ", sock)
                        inputs.remove(sock)
                        sock.close()
                    else:
                        get_request = str(data.decode()).replace("GET /", "GET /pgm6rw/telkom").replace("localhost:9000", f"{people_inf_elte_hu_addr[0]}:{people_inf_elte_hu_addr[1]}").encode()
                        print(get_request)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                            server.connect(people_inf_elte_hu_addr)
                            server.send(get_request)
                            html = server.recv(65000)
                            sock.send(html)
    except KeyboardInterrupt:
        print("Closing the server...")
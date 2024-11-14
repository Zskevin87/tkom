import socket, sys, threading, time

class CheckSum:
    checksum_data = {}

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.__Setup_Server__()

    def __Setup_Server__(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)

        threading.Thread(target=self.__handle_expiration__, daemon=True).start()

        print(f"The CheckSum server is set up on {self.ip}:{self.port}")

        try:
            while True:
                client_socket, _ = server.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except KeyboardInterrupt:
            print("Closing the CheckSum server...")

    def __handle_expiration__(self):
        while True:
            self.current_time = time.time()
            expired_keys = [key for key, value in (self.checksum_data).items() if self.current_time > value[1]]
            for key in expired_keys:
                del self.checksum_data[key]
            time.sleep(1)

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        parts = request.split('|')

        if parts[0] == "BE":
            file_id = parts[1]
            expiration = int(parts[2])
            checksum_length = int(parts[3])
            checksum = parts[4]
            expiration_time = time.time() + expiration
            self.checksum_data[file_id] = (checksum, expiration_time)
            client_socket.send("OK".encode())

        elif parts[0] == "KI":
            file_id = parts[1]
            if file_id in self.checksum_data:
                checksum, _ = self.checksum_data[file_id]
                response = f"{len(checksum)}|{checksum}"
            else:
                response = "0|"
            client_socket.send(response.encode())

        client_socket.close()


if len(sys.argv) != 3:
    print("Usage: python3 checksum_srv.py <ip> <port>")
else:
    checksum = CheckSum(sys.argv[1], int(sys.argv[2]))
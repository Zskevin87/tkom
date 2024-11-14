import socket, sys, hashlib

class NetCopyServer:

    def __init__(self, srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath):
        self.srv_ip = srv_ip
        self.srv_port = srv_port
        self.chsum_srv_ip = chsum_srv_ip
        self.chsum_srv_port = chsum_srv_port
        self.file_id = file_id
        self.filepath = filepath
        self.__accept_file__()
        self.__check_CheckSum_and_file__()


    def __accept_file__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.srv_ip, self.srv_port))
            server_socket.listen(1)
            client_socket, _ = server_socket.accept()

            with open(self.filepath, "wb") as f:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    f.write(data)
    
    def __check_CheckSum_and_file__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chsum_socket:
            chsum_socket.connect((self.chsum_srv_ip, self.chsum_srv_port))
            chsum_socket.send(f"KI|{self.file_id}".encode())
            response = chsum_socket.recv(1024).decode()
            response_parts = response.split("|")

        if response_parts[0] == "0":
            print("CSUM CORRUPTED")
        else:
            received_checksum = response_parts[1]
            local_checksum = self.calculate_md5(self.filepath)
            if received_checksum == local_checksum:
                print("CSUM OK")
            else:
                print("CSUM CORRUPTED")

    def calculate_md5(self, filename):
        md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()


if len(sys.argv) != 7:
    print("Usage: python3 netcopy_srv.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file_id> <filepath>")
else:
    s = NetCopyServer(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
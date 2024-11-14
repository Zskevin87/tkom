import socket, sys, hashlib

class NetCopyClient:

    def __init__(self, srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath):
        self.srv_ip = srv_ip
        self.srv_port = srv_port
        self.chsum_srv_ip = chsum_srv_ip
        self.chsum_srv_port = chsum_srv_port
        self.file_id = file_id
        self.filepath = filepath
        self.__message_to_NetCopy_server__()

    def __message_to_NetCopy_server__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv_socket:
            srv_socket.connect((self.srv_ip, self.srv_port))
            with open(self.filepath, "rb") as f:
                srv_socket.sendfile(f)

        # Calculation of MD5 and sending it to the server
        checksum = self.calculate_md5(self.filepath)
        checksum_length = len(checksum)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chsum_socket:
            chsum_socket.connect((self.chsum_srv_ip, self.chsum_srv_port))
            message = f"BE|{self.file_id}|60|{checksum_length}|{checksum}"
            chsum_socket.send(message.encode())
            response = chsum_socket.recv(1024).decode()
            print(f"Checksum server response: {response}")

    def calculate_md5(self, filename):
        md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

if len(sys.argv) != 7:
    print("Usage: python3 netcopy_cli.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file_id> <filepath>")
else:
    c = NetCopyClient(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
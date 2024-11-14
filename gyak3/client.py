from socket import socket, AF_INET, SOCK_STREAM
import sys

# # Handle port number
# try:
#     port = int(sys.argv[1])
# except:
#     print('Not a number!')


# Creating socket
sock = socket(AF_INET, SOCK_STREAM)
# kliensen ugyanannak a socket-nek kell letrejonnie, 
# mint a szerveren

# itt csak csatlakozni kell egy megadott ipcimre es portszamra

addr = ('127.0.0.1', 8000)
sock.connect(addr)

# Sending data
sock.send('Hello server!'.encode()) # byte literal kuldese 
# (5+1 byte jelenleg (vegen +1 a null literal))

# Receiving data
data = sock.recv(16)
print(data.decode())

sock.close()

# MINDIG A SZERVERT KELL ELOSZOR ELINDITANI!!



# HIBAKEZELES:
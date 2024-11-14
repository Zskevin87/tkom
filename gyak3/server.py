from socket import socket, AF_INET, SOCK_STREAM
import sys

'''
port = 0
# Handle port number
try:
    port = int(sys.argv[1])
except:
    print('Not a number!')
'''

# Creating and binding socket

sock = socket(AF_INET, SOCK_STREAM)
# nekunk csak az adattal kell foglalkozni, 
# a tobbi headert az OS kitolti

addr = ('127.0.0.1', 8000) # ip cim sajat halozati kartya
sock.bind(addr)
# mostantol figyelni fog a szerver ezen a porton erre az ip cimre
sock.listen(0)

conn_sock, conn_addr = sock.accept()
with conn_sock as c:
    print(f'Connected user: {conn_addr}')
    data = conn_sock.recv(16) # 16 byte fogadasa
    print(data.decode())

    conn_sock.send("Hello kliens!".encode())

sock.close()

# MINDIG A SZERVERT KELL ELOSZOR ELINDITANI!!



# HIBAKEZELES:
# socket-nek tilos nevezni barmilyen fajlt! 
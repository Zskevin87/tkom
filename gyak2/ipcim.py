import socket

#print(socket.gethostname("wwww.example.org"))


myname = socket.gethostname()
print(socket.gethostbyname_ex(myname))

print()

hostname, aliases, addrs = socket.gethostbyname_ex("172.18.32.1")
print(hostname, aliases, addrs)
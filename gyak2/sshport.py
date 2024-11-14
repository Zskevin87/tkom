import socket

#1024-ig lefoglaltak, utana szabadon valaszthato (nem minden esetben)

for i in range(1024):
    try:
        print(socket.getservbyport(i))
    except OSError:
        pass


print()

print(socket.getservbyport(21)) #ftp portja
print(socket.getservbyport(22)) #ssh portja
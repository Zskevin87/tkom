import struct

s = "abc".encode()
s2 = s.decode()
print(s,s2)

values = (1, "ab".encode(), 2.7)
packer = struct.Struct("i 2s f") # int, char[2], float
packed_data = packer.pack(*values)
print(packed_data) # b'\x01\x00\x00\x00ab\x00\x00\xcd\xcc,@'

print(packer.size)
print(struct.calcsize("12sf"))

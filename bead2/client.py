

import sys, struct

# [b'987654321', 42, 128.16, True, b'H']

class Client:
    file1 = 0
    file2 = 0
    file3 = 0
    file4 = 0

    format1 = 0
    format2 = 0
    format3 = 0
    format4 = 0

    packer = 0

    def __init__(self, file1, file2, file3, file4, format1, format2, format3, format4) -> None:
        try:
            self.file1 = file1
            self.file2 = file2
            self.file3 = file3
            self.file4 = file4

            self.format1 = format1
            self.format2 = format2
            self.format3 = format3
            self.format4 = format4

            # print(unpacked_data[0])
            # input("Press ENTER To Exit Code...")
            for i in range(4):
                match i+1:
                    case 1:
                        self.__readAndPrintUnpack__(self.file1, format1)
                    case 2:
                        self.__readAndPrintUnpack__(self.file2, format2)
                    case 3:
                        self.__readAndPrintUnpack__(self.file3, format3)
                    case 4:
                        self.__readAndPrintUnpack__(self.file4, format4)
                    
                    case _:
                        raise Exception()
            
            self.__printPacker__()
        except:
            print("Something went wrong... :(")
            exit(-1)

    def __readAndPrintUnpack__(self, file_name, format):
        with open(file_name, 'rb') as file:
            readFile = file.read(struct.calcsize(format))
            unpackedData = struct.unpack(format, readFile)
            print(unpackedData)
            
    def __printPacker__(self):
        string = 0
        packer = 0

        for i in range(4):
            match i:
                case 0:
                    string = ("elso".encode(), 86, True)
                    packer = struct.Struct("18si?")
                    packer_data = packer.pack(*string)
                    print(packer_data)
                case 1:
                    string = (89.5, False, 'X'.encode())
                    packer = struct.Struct("f?c")
                    packer_data = packer.pack(*string)
                    print(packer_data)
                case 2:
                    string = (77, "masodik".encode(), 96.9)
                    packer = struct.Struct("i16sf")
                    packer_data = packer.pack(*string)
                    print(packer_data)
                case 3:
                    string = ('Z'.encode(), 108, "harmadik".encode())
                    packer = struct.Struct("ci19s")
                    packer_data = packer.pack(*string)
                    print(packer_data)
                
                case _:
                    raise Exception()


if len(sys.argv) != 5:
    print("Not enough/too much argument")
    exit(-1)
else:
    client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], '9sif', 'f?c', 'ci9s', 'f9s?')


'''
import struct

# A paraméterek formátuma
format1 = '9sif'  # 9 hosszú string, integer, float
format2 = 'f?c'   # float, bool, karakter
format3 = 'ci9s'  # karakter, integer, 9 hosszú string
format4 = 'f9s?'  # float, 9 hosszú string, bool

# Az összesített formátum (az első rekord tartalmazza mind a négy paramétert)
full_format = format1 + format2 + format3 + format4

# A fájl megnyitása és az első rekord olvasása
with open('database.bin', 'rb') as file:
    # Olvassuk be a teljes rekordot
    record = file.read(struct.calcsize(full_format))
    
    # Csomagoljuk ki az adatokat a megadott formátum szerint
    unpacked_data = struct.unpack(full_format, record)

    # Az unpack visszatérési értéke
    print(unpacked_data)

input("ENTER")
'''
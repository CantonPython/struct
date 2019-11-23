import sys
import struct

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = f.read()

    if len(data) < 8:
        print('not a png file; too short')
        return

    magic = struct.unpack('!B3s4B', data[0:8])
    print('magic:', magic)
    if magic[0] != 0x89:
        print('not a png file; bad magic[0]')
        return
    if magic[1] != b'PNG':
        print('not a png file; bad magic[1]')
        return

    print(filename, 'looks like a png file')

if __name__ == '__main__':
    main()

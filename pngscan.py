import sys
from struct import pack,unpack

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        data = f.read()

    if len(data) < 8:
        print('not a png file; too short')
        return

    magic = unpack('!B3s4B', data[0:8])
    print('magic:', magic)
    if magic[0] != 0x89:
        print('not a png file; bad magic[0]')
        return
    if magic[1] != b'PNG':
        print('not a png file; bad magic[1]')
        return

    print(filename, 'looks like a png file')

    print('chunk')
    address = 8
    while address < len(data):
        print('address', address)

        start = address
        end = address + 8
        chunk_header = unpack('!I4s', data[start:end])
        print('chunk_header', chunk_header)

        start = end
        end = start + chunk_header[0]
        chunk_data = data[start:end]
        if chunk_header[1] == b'iTXt':
            print('chuck_data', chunk_data)

        start = end
        end = start + 4
        crc, = unpack('!I', data[start:end])
        print('crc', crc)
        address = end

if __name__ == '__main__':
    main()

#
# Scan PNG file chunks.
#

import sys
import struct
import binascii

def png_open(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    magic = struct.unpack('!B 3s 4B', data[0:8])
    if magic[0] != 0x89:
        raise ValueError('Not a png file!')
    if magic[1] != b'PNG':
        raise ValueError('Not a png file!')
    return data

def png_chunk(data, address):
    i,j = (address, address+8)
    chunk_len,chunk_type = struct.unpack('!I 4s', data[i:j])
    i,j = (j, j+chunk_len+4)
    chunk_data,chunk_crc = struct.unpack('!{0}s I'.format(chunk_len), data[i:j])
    crc = binascii.crc32(chunk_type)
    crc = binascii.crc32(chunk_data, crc)
    if (crc != chunk_crc):
        raise ValueError('Bad CRC address {0}.'.format(address))
    return (address, j, chunk_type.decode('ascii'), chunk_data)

def png_chunks(data):
    address = 8
    while address < len(data):
        chunk = png_chunk(data, address)
        address = chunk[1]
        yield chunk

def main():
    if len(sys.argv) != 2:
        print('usage: pngscan <filename>')
        return
    data = png_open(sys.argv[1])
    for chunk in png_chunks(data):
        print(chunk[0], chunk[2], chunk[3][0:12])

if __name__ == '__main__':
    main()

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

def png_chunks(data, find='*'):
    address = 8
    while address < len(data):
        chunk = png_chunk(data, address)
        address = chunk[1]
        if find == '*' or chunk[2] == find:
            yield chunk

def png_decode(chunk):
    if chunk[2] == 'IHDR':
        return png_decode_IHDR(chunk[3])
    if chunk[2] == 'tEXt':
        return png_decode_tEXt(chunk[3])
    raise ValueError('Unknown chunk type {0} address'.format(chunk[2],chunk[0]))

def png_decode_IHDR(chunk_data):
    """
    IHDR
    Width   4 bytes
    Height  4 bytes
    Bit depth   1 byte
    Colour type 1 byte
    Compression method  1 byte
    Filter method   1 byte
    Interlace method    1 byte
    """
    return struct.unpack('!2I5B', chunk_data)

def png_decode_tEXt(chunk_data):
    keyword,text = chunk_data.decode('ascii').split('\0')
    return keyword,text

def main():
    if len(sys.argv) != 2:
        print('usage: pngscan <filename>')
        return
    data = png_open(sys.argv[1])

    print('chunks:')
    for chunk in png_chunks(data):
        print(chunk[0], chunk[2], chunk[3][0:12])

    print('text info:')
    for chunk in png_chunks(data, find='tEXt'):
        keyword,text = png_decode(chunk)
        print(keyword, text)

    print('image header:')
    chunk = png_chunk(data, 8)
    if chunk[2] == 'IHDR':
        ihdr = png_decode_IHDR(chunk[3])
        print('  width:', ihdr[0])
        print('  height:', ihdr[1])
        print('  bit depth:', ihdr[2])
        print('  color type:', ihdr[3])
        print('  compression method:',ihdr[4])
        print('  filter method:', ihdr[5])
        print('  interlace method:', ihdr[6])

if __name__ == '__main__':
    main()

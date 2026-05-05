# -*- coding: utf-8 -*-
"""
LevelDB WAL parser - debug v2: check CRC by brute force
"""
import struct, zlib, json, os

LOG_FILE = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000026.log"

with open(LOG_FILE, 'rb') as f:
    data = f.read()

# First 7 bytes
hdr = data[:7]
print(f"Header (7 bytes): {hdr.hex()}")
print(f"  byte[0]: 0x{hdr[0]:02x} (type?)")
print(f"  bytes[1:3]: {hdr[1:3].hex()} -> LE={struct.unpack('<H', hdr[1:3])[0]}, BE={struct.unpack('>H', hdr[1:3])[0]}")
print(f"  bytes[3:7]: {hdr[3:7].hex()} -> LE=0x{struct.unpack('<I', hdr[3:7])[0]:08x}, BE=0x{struct.unpack('>I', hdr[3:7])[0]:08x}")

len_le = struct.unpack('<H', hdr[1:3])[0]
len_be = struct.unpack('>H', hdr[1:3])[0]
crc_le = struct.unpack('<I', hdr[3:7])[0]
crc_be = struct.unpack('>I', hdr[3:7])[0]

print(f"\nCRC32 of data with length={len_le} (LE): computed=0x{zlib.crc32(data[7:7+len_le]):08x} vs header_LE=0x{crc_le:08x}")
print(f"CRC32 of data with length={len_le} (LE): computed=0x{zlib.crc32(data[7:7+len_le]):08x} vs header_BE=0x{crc_be:08x}")
print(f"CRC32 of data with length={len_be} (BE): computed=0x{zlib.crc32(data[7:7+len_be]):08x} vs header_LE=0x{crc_le:08x}")
print(f"CRC32 of data with length={len_be} (BE): computed=0x{zlib.crc32(data[7:7+len_be]):08x} vs header_BE=0x{crc_be:08x}")

# Try: CRC(4) + Type(1) + Length(2) — CRC at bytes 0-3
print(f"\n--- CRC(4) + Type(1) + Length(2) LE ---")
print(f"CRC LE = 0x{struct.unpack('<I', hdr[0:4])[0]:08x}")
print(f"Type = 0x{hdr[4]:02x}")
print(f"Length LE = {struct.unpack('<H', hdr[5:7])[0]}, BE = {struct.unpack('>H', hdr[5:7])[0]}")

l1 = struct.unpack('<H', hdr[5:7])[0]
l2 = struct.unpack('>H', hdr[5:7])[0]
print(f"CRC of data[{7}:{7+l1}] = 0x{zlib.crc32(data[7:7+l1]):08x}")
print(f"CRC of data[{7}:{7+l2}] = 0x{zlib.crc32(data[7:7+l2]):08x}")

# Try: Type + Length(LE) + CRC(4) — Type at byte 0
print(f"\n--- Type(1) + Length(2 LE) + CRC(4) ---")
print(f"Type = 0x{hdr[0]:02x}")
print(f"Length LE = {struct.unpack('<H', hdr[1:3])[0]}")
print(f"CRC LE = 0x{struct.unpack('<I', hdr[3:7])[0]:08x}")
l3 = struct.unpack('<H', hdr[1:3])[0]
crc3 = struct.unpack('<I', hdr[3:7])[0]
computed = zlib.crc32(data[7:7+l3]) & 0xFFFFFFFF
print(f"CRC computed = 0x{computed:08x} vs header CRC = 0x{crc3:08x} -> {'OK' if computed==crc3 else 'MISMATCH'}")

# Try: Length(4 LE) + CRC(4) + Type(1) — unusual
# What if first 4 bytes are a 32-bit length?
len4_le = struct.unpack('<I', hdr[0:4])[0]
print(f"\n--- Length as 4-byte LE = {len4_le} ---")

# Check the actual data
print(f"\n--- Actual record data (first 150 bytes, hex) ---")
print(data[7:157].hex())

# Try decoding as UTF-8
try:
    text = data[7:7+1000].decode('utf-8')
    print(f"\nUTF-8 text (first 500 chars): {text[:500]}")
except:
    print("Not valid UTF-8")

# Check if there are null bytes — if not, maybe data is snappy compressed
has_nulls = b'\x00' in data[7:7+200]
print(f"\nHas null bytes in first 200 bytes of data: {has_nulls}")

# Check the CRC from different positions
print(f"\n--- Check what 'next record' looks like ---")
# If current record is 11886 bytes, next = 7+11886 = 11893
next_pos = 7 + 11886
print(f"Bytes at {next_pos}: {data[next_pos:next_pos+14].hex()}")

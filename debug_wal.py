# -*- coding: utf-8 -*-
"""
LevelDB WAL parser - debugging version
"""
import struct, zlib, json, os

LOG_FILE = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000026.log"

with open(LOG_FILE, 'rb') as f:
    data = f.read()

print(f"File size: {len(data):,} bytes")
print(f"First 100 bytes hex: {data[:100].hex()}")

# Try parsing first block manually
# Block header is 7 bytes: type(1) + length(2) + crc(4)
block_num = 0
pos = 0
block_size = 32 * 1024

while pos < len(data):
    print(f"\n=== Block {block_num} at pos {pos} ===")
    remaining_in_file = len(data) - pos
    block_end = min(pos + block_size, len(data))
    
    record_pos = pos
    records_in_block = 0
    
    while record_pos < block_end - 7:
        block_type = data[record_pos]
        length = struct.unpack_from('>H', data, record_pos + 1)[0]
        crc = struct.unpack_from('>I', data, record_pos + 3)[0]
        header_end = record_pos + 7
        record_end = header_end + length
        
        print(f"  Record @ {record_pos}: type={block_type}, length={length}, crc=0x{crc:08x}, data_range=[{header_end},{record_end}], block_end={block_end}")
        
        if length > 100000 or record_end > block_end + 1000:
            print(f"    -> Suspicious, stopping block parse")
            break
        
        if record_end <= block_end:
            record_data = bytes(data[header_end:record_end])
            # Verify
            computed = zlib.crc32(record_data) & 0xFFFFFFFF
            status = "OK" if computed == crc else f"CRC MISMATCH (got 0x{computed:08x})"
            
            # Try decode
            try:
                text = record_data.decode('utf-8')
                preview = text[:150].replace('\n', '↵')
                print(f"    -> {status}, text: {preview}")
            except:
                print(f"    -> {status}, binary ({len(record_data)} bytes), hex: {record_data[:50].hex()}")
            
            record_pos = record_end
            records_in_block += 1
        else:
            print(f"    -> Record spans to next block, stopping block parse")
            break
    
    print(f"  Records in block: {records_in_block}")
    pos += block_size
    block_num += 1
    
    if block_num > 3:
        print("... stopping after 3 blocks for debug")
        break

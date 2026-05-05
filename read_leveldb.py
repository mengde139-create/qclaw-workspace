# -*- coding: utf-8 -*-
"""
Read leveldb log files (WAL format) to extract flomo memos.
LevelDB log format: https://github.com/google/leveldb/blob/main/doc/log_format.md
"""
import struct, json, os, re

LOG_FILE = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000026.log"

with open(LOG_FILE, 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes ({len(data)/1024:.1f} KB)")

pos = 0
records = []

while pos < len(data):
    # Read block header (32 bytes)
    if pos + 6 > len(data):
        break
    
    # Block is ~32KB, starts with checksum+type
    # Try to find record starts: first 4 bytes are checksum, then block_type
    # block_type: 0=full, 1=first, 2=middle, 3=last
    
    block_type = data[pos]
    length = struct.unpack_from('>H', data, pos + 2)[0]  # big-endian length
    
    if length > 2*1024*1024:  # sanity check
        pos += 1
        continue
    
    if pos + 6 + length > len(data):
        # Try next position
        pos += 1
        continue
    
    payload = data[pos+6:pos+6+length]
    
    # block_type 0=first record, 3=last record, combined they form a full record
    # Actually in the log format: 
    # block_type values: 0=full, 1=first, 2=middle, 3=last
    # 0 = this record is the full record for that key (no previous fragments)
    # 1 = this is the first fragment of a multi-record entry
    # 2 = middle fragment
    # 3 = last fragment
    
    if block_type == 0:
        # Full record - try to parse as leveldb record
        try:
            parsed = parse_record(payload)
            if parsed:
                records.extend(parsed)
        except Exception as e:
            pass
    
    pos += 1

print(f"\nExtracted {len(records)} records")

# Try to find JSON-like memo content
memos = []
for rec in records:
    rec_str = str(rec)
    # Look for memo-like content
    if any(k in rec_str for k in ['"content"', '"created_at"', '"source"', '"tags"']):
        memos.append(rec_str)

print(f"Found {len(memos)} potential memo records")
for m in memos[:5]:
    print(f"\n--- {m[:300]} ---")

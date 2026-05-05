# -*- coding: utf-8 -*-
"""
Parse leveldb WAL (Write-Ahead Log) format.
Format spec: https://github.com/google/leveldb/blob/main/doc/log_format.md

Each 32KB block:
  header: 7 bytes
    block_type: 1 byte  (0=full, 1=first, 2=middle, 3=last)
    length: 2 bytes (uint32 big-endian) — length of data
    crc32: 4 bytes (big-endian)
  data: 'length' bytes

Records can span multiple blocks (first/middle/last).
"""
import struct, zlib, json, os, sys

def read_varint(data, pos):
    result = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, pos
        shift += 7

def decode_key(data):
    """Decode a leveldb key: varint key_size + key_data"""
    try:
        key_size, pos = read_varint(data, 0)
        key_data = data[pos:pos+key_size]
        return key_data.decode('utf-8', errors='replace'), pos + key_size
    except:
        return data.decode('utf-8', errors='replace'), len(data)

def decode_value(data, pos):
    """Decode a leveldb value: varint value_size + value_data"""
    try:
        val_size, new_pos = read_varint(data, pos)
        val_data = data[new_pos:new_pos+val_size]
        return val_data, new_pos + val_size
    except:
        return data[pos:], len(data)

def parse_log_file(filepath):
    records = []
    errors = []
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File: {os.path.basename(filepath)}, size: {len(data):,} bytes")
    
    # Walk through the data 32KB at a time
    block_size = 32 * 1024
    pos = 0
    block_num = 0
    
    while pos < len(data):
        remaining = len(data) - pos
        current_block_size = min(block_size, remaining)
        
        # Parse records within this block
        block_end = pos + current_block_size
        record_pos = pos
        
        while record_pos < block_end - 7:  # Need at least 7 bytes for header
            block_type = data[record_pos]
            length = struct.unpack_from('>H', data, record_pos + 1)[0]
            crc = struct.unpack_from('>I', data, record_pos + 3)[0]
            
            header_end = record_pos + 7
            record_end = header_end + length
            
            if record_end > block_end:
                # Record spans to next block — skip for now
                break
            
            record_data = bytes(data[header_end:record_end])
            
            # Verify CRC32
            computed_crc = zlib.crc32(record_data) & 0xFFFFFFFF
            valid = (computed_crc == crc)
            
            if block_type == 0:  # Full record
                try:
                    records.append(('full', record_data))
                except Exception as e:
                    errors.append(str(e))
            
            record_pos = record_end
        
        pos += current_block_size
        block_num += 1
    
    return records, errors

def extract_memos(records):
    """Extract memo-like records from leveldb records"""
    memos = []
    
    for rec_type, data in records:
        try:
            text = data.decode('utf-8', errors='replace')
            
            # Check if it looks like a JSON object
            if text.strip().startswith('{'):
                try:
                    obj = json.loads(text)
                    # Check for memo-like fields
                    if any(k in obj for k in ['content', 'created_at', 'id', 'source', 'user_id']):
                        memos.append(obj)
                        continue
                except json.JSONDecodeError:
                    pass
            
            # Also check raw text for content patterns
            if 'content' in text and len(text) > 50:
                memos.append({'raw': text[:200]})
                
        except Exception as e:
            pass
    
    return memos

# Parse all log files
log_dir = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb"
log_files = sorted([f for f in os.listdir(log_dir) if f.endswith('.log')])
print(f"Found {len(log_files)} log files: {log_files}")

all_records = []
for lf in log_files:
    records, errors = parse_log_file(os.path.join(log_dir, lf))
    print(f"  -> {len(records)} records, {len(errors)} errors")
    all_records.extend(records)

print(f"\nTotal records: {len(all_records)}")

memos = extract_memos(all_records)
print(f"Found {len(memos)} potential memos")

for m in memos[:10]:
    print(f"\n--- {str(m)[:300]} ---")

# -*- coding: utf-8 -*-
"""
LevelDB SSTable (.ldb) parser.
SSTable format: https://github.com/google/leveldb/blob/main/doc/table_format.md

Each block:
  - data: compressed or raw
  - type: 1 byte (0=raw, 1=snappy, etc.)
  - crc32: 4 bytes

Block size is stored in the index block.
We can also try to read blocks directly.
"""
import struct, zlib, json, os

LDB_DIR = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb"

# Files and sizes
for f in sorted(os.listdir(LDB_DIR)):
    if f.endswith('.ldb'):
        path = os.path.join(LDB_DIR, f)
        with open(path, 'rb') as fh:
            data = fh.read(100)
        print(f"{f}: {os.path.getsize(path)/1024:.1f} KB, first_bytes: {data[:20].hex()}")
    elif f.endswith('.log'):
        path = os.path.join(LDB_DIR, f)
        print(f"{f}: {os.path.getsize(path)/1024:.1f} KB")

print()

# The SSTable has a specific footer (metaindex + index blocks at the end)
# Let me try to read the MANIFEST to understand the structure
manifest_path = os.path.join(LDB_DIR, 'MANIFEST-000001')
if os.path.exists(manifest_path):
    with open(manifest_path, 'rb') as f:
        content = f.read()
    print(f"MANIFEST: {len(content)} bytes, first 200 hex: {content[:200].hex()}")
    # Try to find "flomo" strings
    text = content.decode('utf-8', errors='replace')
    for chunk in text.split('\x00'):
        if 'flomo' in chunk or 'memo' in chunk.lower():
            print(f"  Found: {chunk[:100]}")

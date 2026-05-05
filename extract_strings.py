# -*- coding: utf-8 -*-
"""
Extract readable strings from leveldb log/WAL files.
LevelDB stores data with internal records. We'll extract strings by scanning
for valid UTF-8 sequences.
"""
import re, json, os

files = [
    (r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000026.log", "WAL log"),
    (r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000028.ldb", "SSTable 1"),
    (r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb\000029.ldb", "SSTable 2"),
]

all_memos = []

for fpath, desc in files:
    if not os.path.exists(fpath):
        continue
    size = os.path.getsize(fpath)
    print(f"\n{'='*60}")
    print(f"File: {os.path.basename(fpath)} ({size/1024:.1f} KB) - {desc}")
    print('='*60)
    
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Try UTF-8 decode
    text = raw.decode('utf-8', errors='replace')
    
    # Extract strings: sequences of printable chars longer than 20
    # that look like memo content
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if len(line) > 30:
            # Check if it looks like JSON with content field
            if '"content"' in line or '"created_at"' in line or '"source"' in line:
                # Try to extract JSON
                try:
                    # Find JSON-like objects
                    idx = line.find('"content"')
                    if idx >= 0:
                        snippet = line[max(0,idx-50):idx+500]
                        print(f"  Block {i} (around content): {snippet[:400]}")
                        print()
                except:
                    pass
    
    # Also look for long consecutive strings
    # Find sequences of Chinese chars or mixed content
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\w\s]{50,}')
    matches = chinese_pattern.findall(text)
    
    interesting = []
    for m in matches:
        m = m.strip()
        # Filter out noise
        if len(m) < 30:
            continue
        if m.startswith('#') or m.startswith('//') or m.startswith('/*'):
            continue
        if any(noise in m for noise in ['\\\\x', '\\\\n', '\\u00', 'http://', 'https://']):
            # Check if it's really noise
            if '\\x' in m or '\\u00' in m:
                continue
        interesting.append(m)
    
    print(f"\n  Found {len(interesting)} interesting strings")
    for s in interesting[:5]:
        print(f"  String ({len(s)} chars): {s[:200]}")

print("\n\nDone scanning files.")

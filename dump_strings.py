# -*- coding: utf-8 -*-
"""
Search for readable strings (memo content) in binary leveldb files.
"""
import re, os

LDB_DIR = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\IndexedDB\flomo_._0.indexeddb.leveldb"

files = {
    '000026.log': os.path.join(LDB_DIR, '000026.log'),
    '000028.ldb': os.path.join(LDB_DIR, '000028.ldb'),
    '000029.ldb': os.path.join(LDB_DIR, '000029.ldb'),
}

for name, path in files.items():
    size = os.path.getsize(path)
    print(f"\n{'='*60}")
    print(f"File: {name} ({size/1024:.1f} KB)")
    print('='*60)
    
    with open(path, 'rb') as f:
        data = f.read()
    
    # Find sequences of Chinese characters and alphanumeric mixed content
    # Look for patterns that indicate memo content
    
    # Pattern 1: Long sequences of Chinese chars
    chinese_seq = re.compile(rb'[\xe4-\xe9][\x80-\xbf][\x80-\xbf]{3,}')
    matches = chinese_seq.findall(data)
    print(f"Chinese sequences (3+ chars): {len(matches)}")
    for m in matches[:3]:
        try:
            print(f"  {m.decode('utf-8')[:100]}")
        except:
            print(f"  (binary): {m.hex()}")
    
    # Pattern 2: Look for "content" as UTF-16 or UTF-8
    # In JSON stored in leveldb: "content":"...or "content": "...
    # Try UTF-16LE (common in some databases)
    try:
        text_utf16 = data.decode('utf-16-le', errors='replace')
        content_matches = re.findall(r'content["""].{10,300}?["""]', text_utf16)
        if content_matches:
            print(f"\nUTF-16 content matches: {len(content_matches)}")
            for m in content_matches[:5]:
                print(f"  {m[:200]}")
    except:
        pass
    
    # Pattern 3: Try to find null-terminated strings
    null_strings = re.findall(rb'[\x20-\x7e\xc0-\xff]{8,}', data)
    interesting = [s for s in null_strings if len(s) > 20 and not s.startswith(b'//') and not s.startswith(b'/*')]
    print(f"\nReadable strings (>20 chars): {len(interesting)}")
    for s in interesting[:10]:
        try:
            print(f"  {s.decode('ascii', errors='replace')[:150]}")
        except:
            pass
    
    # Pattern 4: Look for JSON-like structures
    # Try finding {...} patterns
    print(f"\nSearching for JSON structures...")
    text = data.decode('utf-8', errors='replace')
    
    # Find UTF-8 strings (sequences of printable/semi-printable chars)
    # Use a different approach: scan byte by byte and collect runs
    runs = []
    current = []
    for b in data:
        if 32 <= b < 127 or (b >= 0xC0):  # printable ASCII or start of UTF-8
            current.append(b)
        else:
            if len(current) >= 20:
                runs.append(bytes(current))
            current = []
    if len(current) >= 20:
        runs.append(bytes(current))
    
    print(f"Found {len(runs)} readable runs")
    for run in runs[:10]:
        try:
            s = run.decode('utf-8', errors='replace')
            if any(k in s for k in ['content', 'created', 'source', 'memo', 'tags', '{\\"id\\"']):
                print(f"\n  INTERESTING: {s[:300]}")
        except:
            pass

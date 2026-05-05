# -*- coding: utf-8 -*-
import re, json, os

ldb_files = [
    r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\Local Storage\leveldb\001665.ldb",
    r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\Local Storage\leveldb\001663.ldb",
    r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\Local Storage\leveldb\001661.ldb",
    r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\Local Storage\leveldb\001659.ldb",
    r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\Local Storage\leveldb\000005.ldb",
]

all_memos = []

for fpath in ldb_files:
    if not os.path.exists(fpath):
        continue
    print(f"Reading {os.path.basename(fpath)}...")
    with open(fpath, 'rb') as f:
        data = f.read()
    
    # Try UTF-8
    text = data.decode('utf-8', errors='replace')
    
    # Try to find content patterns
    # Flomo stores memos as JSON strings in localStorage
    # Look for content field with reasonable text length
    pattern = r'"content"\s*:\s*"([^"]{20,2000})"'
    matches = re.findall(pattern, text)
    for m in matches:
        # Unescape common sequences
        clean = m.replace('\\n', '\n').replace('\\"', '"').replace('\\u', '\\\\u')
        if clean.strip() and not clean.startswith('{') and len(clean) > 5:
            all_memos.append(clean)
    
    # Also try to find any long readable strings (more than 50 chars)
    # that aren't hex/binary
    printable_pattern = r'[\x20-\x7e\u4e00-\u9fff]{30,}'
    strings = re.findall(printable_pattern, text)
    for s in strings:
        if s not in all_memos and '\\x' not in s and len(s) > 30:
            # Check if it looks like a memo (not a URL/path/code)
            if not s.startswith('http') and not s.startswith('/') and not s.startswith('function'):
                all_memos.append(s)

print(f"\nTotal potential memos found: {len(all_memos)}")
print("\nSample memos (first 10):")
for i, m in enumerate(all_memos[:10]):
    print(f"\n--- Memo {i+1} ---")
    print(m[:300])

# Save raw extracts
with open(r"C:\Users\mengdejun\.qclaw\workspace\flomo_raw.txt", 'w', encoding='utf-8') as f:
    for m in all_memos:
        f.write(m + '\n\n' + '='*40 + '\n\n')

print("\nSaved raw extracts to flomo_raw.txt")

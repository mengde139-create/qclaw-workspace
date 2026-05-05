# -*- coding: utf-8 -*-
import urllib.request, json, time

api_token = '696fc5dc7ee3ecb216318ce312784f59'

headers = {
    'Authorization': f'Bearer {api_token}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) flomo-desktop/5.26.32 Chrome/120.0.0.0 Electron/30.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://flomoapp.com/',
}

# Try to get a CSRF token first
req = urllib.request.Request('https://flomoapp.com/', headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('Main page status:', resp.status)
        # Check for Set-Cookie
        print('Headers:', dict(resp.headers))
except Exception as e:
    print(f'Main page error: {e}')

print()

# Try the API with the CSRF token from HTML
import re
# Actually, let's just try direct API calls
urls = [
    'https://flomoapp.com/api/v1/memo?api_token=' + api_token + '&limit=5',
    'https://flomoapp.com/api/v1/memo',
]

for url in urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f'URL: {url}')
            print(f'Status: {resp.status}')
            body = resp.read().decode('utf-8', errors='replace')
            print(f'Body (first 500): {body[:500]}')
            print()
            # Try JSON
            try:
                data = json.loads(body)
                print(f'JSON: {json.dumps(data, ensure_ascii=False)[:500]}')
            except:
                pass
    except Exception as e:
        print(f'URL: {url} -> Error: {e}')
        print()

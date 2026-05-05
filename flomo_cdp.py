# -*- coding: utf-8 -*-
"""
Connect to flomo desktop app via CDP and automate the export.
"""
import subprocess, sys, json, time

# Ensure websockets is available
try:
    import websockets
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'websockets', '-q'])
    import websockets

import asyncio

CDP_URL = "ws://localhost:9222/devtools/browser/b49bfd82-2665-4446-9543-4ee4f3922b33"

async def main():
    async with websockets.connect(CDP_URL, max_size=50*1024*1024) as ws:
        # Send CDP list_tabs
        await ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))
        raw = await ws.recv()
        data = json.loads(raw)
        print("Targets:", json.dumps(data, indent=2, ensure_ascii=False))
        
        # Find flomo tab
        targets = data.get('result', {}).get('targetInfos', [])
        flomo_tab = None
        for t in targets:
            if 'flomo' in t.get('title', '').lower() or 'flomo' in t.get('url', '').lower():
                flomo_tab = t
                break
        
        if not flomo_tab:
            print("No flomo tab found. Available targets:")
            for t in targets:
                print(f"  - {t.get('title','')} | {t.get('url','')}")
            return
        
        print(f"\nFound flomo tab: {flomo_tab['targetId']}")
        tab_id = flomo_tab['targetId']
        
        # Attach to tab
        await ws.send(json.dumps({
            "id": 2, 
            "method": "Target.attachToTarget",
            "params": {"targetId": tab_id, "flatten": True}
        }))
        raw = await ws.recv()
        print("Attach response:", raw[:500])
        
        # Get URL
        await ws.send(json.dumps({"id": 3, "sessionId": tab_id, "method": "Runtime.evaluate", "params": {"expression": "window.location.href"}}))
        raw = await ws.recv()
        print("URL:", raw[:300])

if __name__ == '__main__':
    asyncio.run(main())

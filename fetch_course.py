import sys, os, time
sys.path.insert(0, r'C:\Program Files\QClaw\resources\openclaw\config\skills\browser-cdp\scripts')

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
from cdp_client import CDPClient
from page_snapshot import PageSnapshot
from browser_actions import BrowserActions

launcher = BrowserLauncher()
try:
    cdp_url = launcher.launch(browser='chrome')
except BrowserNeedsCDPError as e:
    print(f"BROWSER_NEEDS_CDP: {e}")
    sys.exit(1)

client = CDPClient(cdp_url)
client.connect()

# Check existing tabs
target_url = 'https://webapp.songy.info/'
tabs = client.list_tabs()
tab = None
for t in tabs:
    if target_url in t['url']:
        tab = t
        break

if tab:
    client.attach(tab['id'])
else:
    tab = client.create_tab(target_url)
    client.attach(tab['id'])

actions = BrowserActions(client, PageSnapshot(client))
actions.wait_for_load()
time.sleep(3)

# Navigate to the course page
actions.navigate('https://webapp.songy.info/#/courses/details?course_id=775&auto_play=true&last_duration=0')
time.sleep(5)
actions.wait_for_load()

# Get accessibility tree
snapshot = PageSnapshot(client)
tree = snapshot.accessibility_tree()
print(tree[:15000])

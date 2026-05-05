#!/usr/bin/env python3
import win32gui
import win32process
import psutil

def get_all_windows():
    windows = []
    def callback(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    windows.append({'hwnd': hwnd, 'title': title, 'pid': pid})
                except:
                    pass
    win32gui.EnumWindows(callback, None)
    return windows

# Get devtools processes
devtools_pids = set()
for proc in psutil.process_iter(['pid', 'name']):
    try:
        name = proc.info['name'].lower() if proc.info['name'] else ''
        if 'wechatdevtools' in name:
            devtools_pids.add(proc.info['pid'])
    except:
        pass

print(f'DevTools PIDs: {len(devtools_pids)} processes')

# Enumerate all windows
all_windows = get_all_windows()
devtools_windows = [w for w in all_windows if w['pid'] in devtools_pids]

print(f'WeChat DevTools windows: {len(devtools_windows)}')
print()
print('All windows:')
for w in devtools_windows[:20]:
    print(f'  [PID={w["pid"]}] {w["title"]}')

# Find project window
project_wins = [w for w in devtools_windows if 'personal' in w['title'].lower() or '写作' in w['title']]
if project_wins:
    print()
    print('Project windows:')
    for w in project_wins:
        print(f'  HWND={w["hwnd"]} {w["title"]}')
else:
    print()
    print('No project window found')
    print('Titles:', [w['title'] for w in devtools_windows[:10]])

# Check for dialog
dialog_wins = [w for w in devtools_windows if '版本' in w['title'] or '上传' in w['title']]
if dialog_wins:
    print()
    print('Dialog windows:')
    for w in dialog_wins:
        print(f'  HWND={w["hwnd"]} {w["title"]}')

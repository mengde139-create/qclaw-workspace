import win32gui
import win32process
import win32con
import psutil
import time

# Get devtools pids
devtools_pids = set()
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if 'wechatdevtools' in proc.info['name'].lower():
            devtools_pids.add(proc.info['pid'])
    except:
        pass

project_hwnd = 1903390
main_hwnd = 1313730

# First, let's try to activate the window and send keystrokes
print("=== Step 1: Focus the project window ===")

# Try using PostMessage to bring to front
win32gui.PostMessage(project_hwnd, win32con.WM_ACTIVATE, 1, 0)
time.sleep(0.5)

# Get the foreground window
foreground = win32gui.GetForegroundWindow()
print(f"Current foreground: {foreground}")

# Let's try using SendMessage instead
print("\n=== Step 2: Send keyboard shortcut Ctrl+U (upload) ===")

# Check window info
title = win32gui.GetWindowText(project_hwnd)
print(f"Window title: {title}")

# Try Ctrl+U
win32gui.PostMessage(project_hwnd, win32con.WM_KEYDOWN, ord('U'), 0)
win32gui.PostMessage(project_hwnd, win32con.WM_KEYUP, ord('U'), 0)
print("Sent Ctrl+U")

time.sleep(1)

# Check if dialog appeared
def find_dialogs():
    result = []
    def callback(h, ctx):
        try:
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                cls = win32gui.GetClassName(h)
                _, pid = win32process.GetWindowThreadProcessId(h)
                if pid in devtools_pids and h not in [1313730, 1903390]:
                    result.append({'hwnd': h, 'title': title, 'class': cls, 'pid': pid})
        except:
            pass
        return True
    win32gui.EnumWindows(callback, None)
    return result

dialogs = find_dialogs()
if dialogs:
    print(f"\nFound {len(dialogs)} dialog(s):")
    for d in dialogs:
        print(f"  HWND={d['hwnd']} [{d['pid']}] '{d['title']}' Class={d['class']}")
else:
    print("\nNo dialogs found")

# Try alternative: Use the menu via Alt key
print("\n=== Step 3: Try Alt key menu ===")
win32gui.PostMessage(project_hwnd, win32con.WM_SYSKEYDOWN, ord('F'), 0)
time.sleep(0.3)
win32gui.PostMessage(project_hwnd, win32con.WM_SYSKEYUP, ord('F'), 0)
time.sleep(1)

# Try F (File menu)
print("Sent Alt+F")
dialogs2 = find_dialogs()
if dialogs2:
    print(f"Found {len(dialogs2)} dialog(s)")

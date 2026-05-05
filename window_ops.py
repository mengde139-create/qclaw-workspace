import win32gui
import win32process
import win32con

# Get devtools pids
import psutil
devtools_pids = set()
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if 'wechatdevtools' in proc.info['name'].lower():
            devtools_pids.add(proc.info['pid'])
    except:
        pass

# Check for dialogs
def check_dialog():
    hwnd = 131638  # Known dialog from earlier
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        cls = win32gui.GetClassName(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        print(f"Dialog 131638 found: '{title}' Class={cls}")
        print(f"  Rect: {rect}")
        return True
    else:
        print("Dialog 131638 not visible")
        
    # Enumerate all windows to find dialogs
    def enum_callback(h, ctx):
        try:
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                cls = win32gui.GetClassName(h)
                if title or 'dialog' in cls.lower():
                    _, pid = win32process.GetWindowThreadProcessId(h)
                    if pid in devtools_pids:
                        print(f"  HWND={h} [{pid}] '{title}' Class={cls}")
        except:
            pass
        return True
    
    print("All devtools windows:")
    win32gui.EnumWindows(enum_callback, None)
    return False

check_dialog()

# Bring project window to foreground
project_hwnd = 1903390
print(f"\nActivating project window: {project_hwnd}")
win32gui.ShowWindow(project_hwnd, win32con.SW_RESTORE)
win32gui.SetForegroundWindow(project_hwnd)
print("Done")

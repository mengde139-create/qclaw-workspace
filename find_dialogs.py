import win32gui
import win32process
import psutil
import win32con

# Get devtools pids
devtools_pids = set()
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if 'wechatdevtools' in proc.info['name'].lower():
            devtools_pids.add(proc.info['pid'])
    except:
        pass

print(f"DevTools PIDs: {sorted(devtools_pids)}")

def get_all_child_windows(hwnd, max_depth=3, depth=0):
    if depth > max_depth:
        return []
    result = []
    try:
        child = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
        while child:
            try:
                title = win32gui.GetWindowText(child)
                cls = win32gui.GetClassName(child)
                rect = win32gui.GetWindowRect(child)
                visible = win32gui.IsWindowVisible(child)
                if visible:
                    result.append({
                        'hwnd': child,
                        'title': title,
                        'class': cls,
                        'rect': rect,
                        'depth': depth
                    })
                    # Recurse
                    result.extend(get_all_child_windows(child, max_depth, depth+1))
            except:
                pass
            child = win32gui.GetWindow(child, win32con.GW_HWNDNEXT)
    except:
        pass
    return result

# Check main windows
main_windows = {1313730: 'miniprogram', 1903390: 'personal-assistant'}

print("\n=== Child windows ===")
for hwnd, name in main_windows.items():
    print(f"\nMain window: {name} (HWND={hwnd})")
    children = get_all_child_windows(hwnd, max_depth=2)
    print(f"  Found {len(children)} child windows")
    for c in children[:20]:
        print(f"    HWND={c['hwnd']} [{c['class']}] '{c['title']}'")

# Check for any dialog-like windows
print("\n=== Looking for dialogs/popups ===")
def enum_callback(h, ctx):
    try:
        if win32gui.IsWindowVisible(h):
            title = win32gui.GetWindowText(h)
            cls = win32gui.GetClassName(h)
            _, pid = win32process.GetWindowThreadProcessId(h)
            if pid in devtools_pids:
                # Check if it's a popup/dialog
                style = win32gui.GetWindowLong(h, win32con.GWL_STYLE)
                ex_style = win32gui.GetWindowLong(h, win32con.GWL_EXSTYLE)
                is_popup = bool(ex_style & win32con.WS_EX_TOPMOST) or bool(style & win32con.WS_POPUP)
                if title or is_popup:
                    print(f"  HWND={h} [{pid}] '{title}' Class={cls} Popup={is_popup}")
    except:
        pass
    return True

win32gui.EnumWindows(enum_callback, None)

import os
import shutil
import ctypes
from ctypes import wintypes
from datetime import datetime

def get_desktop_path():
    CSIDL_DESKTOP = 0x0000
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOP, 0, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def CleanDesktop():
    desktop_path = get_desktop_path()
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_name = f"Desktop from {date_str}"
    backup_folder_name = base_name
    counter = 1

    while os.path.exists(os.path.join(desktop_path, backup_folder_name)):
        backup_folder_name = f"{base_name} ({counter})"
        counter += 1

    backup_folder_path = os.path.join(desktop_path, backup_folder_name)
    os.makedirs(backup_folder_path, exist_ok=True)

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        if item == backup_folder_name:
            continue
        if os.path.isdir(item_path):
            continue
        item_lower = item.lower()
        if item_lower.endswith(('.lnk', '.zip', '.url', 'cleandesktop.py')):
            continue
        
        try:
            shutil.move(item_path, backup_folder_path)
        except Exception as e:
            continue

    for moved_item in os.listdir(backup_folder_path):
        original_path = os.path.join(desktop_path, moved_item)
        if os.path.exists(original_path):
            try:
                os.remove(original_path)
            except:
                pass

if __name__ == "__main__":
    CleanDesktop()

import os, sys

def path(original_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath('.')
    return os.path.join(base_path, original_path)

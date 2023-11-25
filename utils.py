import os
from constants import *

def organize_entry(entry):
    entry_src_path = os.path.join(os.getcwd(), entry)

    if os.path.isfile(entry):
        type = getTypeByEntry(entry)
        type_dir = make_dir(type)
        entry_dst_path = os.path.join(type_dir, entry)
        os.rename(entry_src_path, entry_dst_path)

    elif os.path.isdir(entry):
        folders_dir = make_dir('folders')
        #here checking if the entry I'm about to organize is any one of the dir for the types
        #destinations is a constant in constants file
        if not any((name in entry for name in DESTINATIONS) or (name in entry for name in SYS_DIRS)): 
            entry_dst_path = os.path.join(folders_dir, entry)
            os.rename(entry_src_path, entry_dst_path)

    else:
        other_dir = make_dir('other')
        entry_dst_path = os.path.join(other_dir, entry)
        os.rename(entry_src_path, entry_dst_path)

def make_dir(name):
    new_dir_path = os.path.join(os.getcwd(), name)

    if os.path.exists(new_dir_path):
            return new_dir_path
    else:
        try:
            os.mkdir(new_dir_path)
            return new_dir_path
        except OSError as error:
            print(error)
            return None

def find_dir(target_name):
    found_dirs = list()
    for root, dirs, files in os.walk('/home/soulaiman', topdown=True, onerror=None, followlinks=False):
        if target_name in dirs:
            wanted_dir_path = os.path.join(root, target_name)
            found_dirs.append(wanted_dir_path)
    
    return found_dirs

def getTypeByEntry(entry):
    for dict in FILE_TYPES_AND_EXTENSIONS:
            if any (
                 ((extension[0] in entry) or ((extension[0].upper() in entry))) 
                 for extension in dict.get("extensions", [])):
                    return dict.get("type")
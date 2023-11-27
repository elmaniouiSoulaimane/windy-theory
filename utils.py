import os
from constants import *

def organize_entry(entry):
    source = os.path.join(os.getcwd(), entry)
    destination = source #if there's no destination that suits the entry, leave it there.

    if os.path.isfile(entry):
        type = getTypeByEntry(entry)
        if type is not None:
            type_dir = make_dir(type)
            destination = os.path.join(type_dir, entry)

    elif os.path.isdir(entry):
        folders_dir = make_dir('folders')

        #TO DO: must also check if the folder I am about to organize is not among the default user dirs
        if not any(name in entry for name in DESTINATIONS): 
            destination = os.path.join(folders_dir, entry)

    else:
        other_dir = make_dir('other')
        destination = os.path.join(other_dir, entry)

    if source != destination:
        os.rename(source, destination)
        return entry
    else:
        return None

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

def find_dir(target):
    found_dirs = list()

    #must get user's name
    for root, dirs, files in os.walk('/home/soulaiman/', topdown=True, onerror=None, followlinks=False):
        if target in dirs:
            target_dir_path = os.path.join(root, target)
            found_dirs.append(target_dir_path)
    
    return found_dirs

def getTypeByEntry(entry):
    for dict in FILE_TYPES_AND_EXTENSIONS:
            if any (
                 ((extension[0] in entry) or ((extension[0].upper() in entry))) 
                 for extension in dict.get("extensions", [])):
                    return dict.get("type")
    return None

def organize(target_name, target_path):
    os.chdir(target_path)
    
    #organizing elements only if they exist
    if len(os.listdir()):
        organized_entries = list()
        for entry in os.listdir():
            organized_entry = organize_entry(entry)
            if organize_entry is not None:
                organized_entries.append(organized_entry)

        #only display this message if there was something to be organized to begin with
        if len(organized_entries):
            print(f"(i) The following entries have been organized successfully!")
            #TO DO: the following loop must be put in a function!
            for entry in organized_entries:
                print(f"{entry}")
        else:
            print(f"(i) Looks like \"{target_name}\" is already organized!")
    else:
        print(f"(i) Oops! \n")
        print(f"(i) Looks like the folder you chose \"{target_name}\" is empty!")
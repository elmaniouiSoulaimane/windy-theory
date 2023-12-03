import os
from constants import *
import pyinputplus as pyip

#LOCAL IMPORTS
from tasks.organize import Organize
from tasks.cleanup import Cleanup

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


def get_target_dir_paths(target_dir):
    found_dirs = list()

    #TO DO: must get user's name
    for root, dirs, files in os.walk('/home/soulaiman/', topdown=True, onerror=None, followlinks=False):
        if target_dir in dirs:
            target_dir_path = os.path.join(root, target_dir)
            found_dirs.append(target_dir_path)
    
    return found_dirs


def get_entry_type(entry):
    for dict in FILE_TYPES_AND_EXTENSIONS:
            if any (
                 ((extension[0] in entry) or ((extension[0].upper() in entry))) 
                 for extension in dict.get("extensions", [])):
                    return dict.get("type")
    return None


def suggest_tasks():
    new_task = pyip.inputMenu([
                            "help",
                            "History",
                            "Cleanup",
                            "Undo an action",
                            "Organize a folder",
                            "Quick Backup",
                            "Quit"
                        ], lettered=False, numbered=True)
    
    #I need to confirm for sensitive options
    if new_task == "help":
        pass

    elif new_task == "Organize a folder":
        task = Organize()
        task.start()

    elif new_task == "Cleanup":
        task = Cleanup
        task.start()

    elif new_task == "Quick Backup":
        pass
    
    elif new_task == "Quit":
        pass
import os
from constants import *


#this needs to be optimized
#currently it loops through all the types
#it should work on the types that are inside the cwd
def organize_type(element, cwd):
    type = element['type']
    extentions = element['extensions']

    print(f"Starting to organize \"{type}\".")

    #creating a directory for the current type
    type_dir = make_dir(type, cwd)

    for entry in os.listdir():
        if os.path.isfile(entry):
            for element in extentions:
                ext = element[0]
                if ext in entry:
                    src_path = os.path.join(cwd, entry)
                    dst_path = os.path.join(type_dir, entry)
                    #sending the current entry to the appropriate folder
                    os.rename(src_path, dst_path) 
        elif os.path.isdir(entry):
            #folders folder is already created, why create it again
            folders_dir = make_dir('folders', cwd)
            
            #here checking if the entry I'm about to organize is any one of the dir for the types
            #destinations is a constant in constants file
            if not any(name in entry for name in DESTINATIONS): 
                src_path = os.path.join(cwd, dir)
                dst_path = os.path.join(folders_dir, dir)
                os.rename(src_path, dst_path)
        else:
            #other folder is already created, why create it again
            other_dir = make_dir('other', cwd)
            src_path = os.path.join(cwd, dir)
            dst_path = os.path.join(other_dir, dir)
            os.rename(src_path, dst_path)

def make_dir(name, cwd): #add src dir as an argument
    new_dir_path = os.path.join(cwd, name)

    if os.path.exists(new_dir_path):
            print(f'"{new_dir_path}" exists!')
            return new_dir_path
    else:
        print(f'"{new_dir_path}" does not exist. Lets try to make it.')
        try:
            os.mkdir(new_dir_path)
            print(f"{new_dir_path} directory created successfuly!")
            return new_dir_path
        except OSError as error:
            print(error)
            return None

def find_dir(target_name):
    #what if multiple directories exists in the computer with the same name ?
    found_dirs = list()
    for root, dirs, files in os.walk('/', topdown=True, onerror=None, followlinks=False):
        if target_name in dirs:
            wanted_dir_path = os.path.join(root, target_name)
            found_dirs.append(wanted_dir_path)
    
    return found_dirs
    
import os
from config import *

def organize_type(element, cwd, folders_dir, other_dir):
    type = element['type']
    extentions = element['extensions']

    print(f"Organizing {type}")

    type_dir = make_dir(type, cwd)

    for dir in os.listdir():
        if os.path.isfile(dir):
            for element in extentions:
                ext = element[0]
                if ext in dir:
                    src_path = os.path.join(cwd, dir)
                    dst_path = os.path.join(type_dir, dir)
                    os.rename(src_path, dst_path)
        elif os.path.isdir(dir):
            if not any(name in dir for name in destinations):
                src_path = os.path.join(cwd, dir)
                dst_path = os.path.join(folders_dir, dir)
                os.rename(src_path, dst_path)
        else:
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
    
    
    
    
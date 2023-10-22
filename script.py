#!/usr/bin/env python3
import os
import json
from utils import make_dir, organize_type, find_dir

cwd = os.getcwd()  
print("Current working directory:", cwd)


target_name = 'traditional-hat-set'
target_path = find_dir('/', target_name)
print(f"the path for {target_name} is => {target_path}")

"""with open('data.json', 'r') as data:
    files_data = json.load(data)

    if cwd is not downloads_dir:
        os.chdir(downloads_dir)
        cwd = os.getcwd()
    
    folders_dir = make_dir('folders', cwd)
    other_dir = make_dir('other', cwd)

    for element in files_data:
        organize_type(element, cwd, folders_dir, other_dir)"""


    


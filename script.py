#!/usr/bin/env python3
import os
import json
from utils import make_dir, organize_type

cwd = os.getcwd()  
print("Current working directory:", cwd)

downloads_dir = "../../../Downloads"

with open('data.json', 'r') as data:
    files_data = json.load(data)

    if cwd is not downloads_dir:
        os.chdir(downloads_dir)
        cwd = os.getcwd()
    
    folders_dir = make_dir('folders', cwd)
    other_dir = make_dir('other', cwd)

    for element in files_data:
        organize_type(element, cwd, folders_dir, other_dir)


    


#!/usr/bin/env python3
import os
import json
from utils import *

cwd = os.getcwd()  
print("Current working directory:", cwd)

downloads_dir = "../../../Downloads"

with open('data.json', 'r') as data:
    files_data = json.load(data)

    if cwd is not downloads_dir:
        os.chdir(downloads_dir)
        cwd = downloads_dir = os.getcwd() 

    for element in files_data:
        organize_type(cwd, downloads_dir, element)
    


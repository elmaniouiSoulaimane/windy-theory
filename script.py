#!/usr/bin/env python3
import os
import json
import argparse
from utils import make_dir, organize_type, find_dir

def main():

    target_name = input("Type in the name of the folder you want to organize: ")
    target_path = find_dir('/', target_name)

    cwd = os.getcwd()

    with open('data.json', 'r') as data:
        files_data = json.load(data)

        if cwd is not target_path:
            os.chdir(target_path)
            cwd = os.getcwd()
        
        folders_dir = make_dir('folders', cwd)
        other_dir = make_dir('other', cwd)

        for element in files_data:
            organize_type(element, cwd, folders_dir, other_dir)

if __name__ == "__main__":
    main()


    


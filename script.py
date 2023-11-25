#!/usr/bin/env python3
import os
import json
import argparse
from utils import make_dir, organize_type, find_dir

def main():

    #1-GET THE WANTED DISTINATION
    target_name = input("Type in the name of the folder you want to organize: ")
    target_paths = find_dir(target_name)
    target_path = None

    if len(target_paths) > 1:
        print(f"*i* It seems like there are multiple folders in your computer that are named \"{target_name}\".")
        print("*i* Here are the paths for each folder that I found:")
        counter = 0
        for item in target_paths:
            counter += 1
            print(f"*i* {counter}-{item}")
    
        item_index = input("*i* Type the number of the wanted destination:")
        target_path = target_path[item_index]
    else:
        target_path = target_paths[0]

    cwd = os.getcwd()

    with open('data.json', 'r') as data:
        files_data = json.load(data)

        if cwd is not target_path:
            os.chdir(target_path)
            cwd = os.getcwd()
        
        folders_dir = make_dir('folders', cwd) #why do I need to create this ?
        other_dir = make_dir('other', cwd) #why do I need to create this ?

        for element in files_data:
            organize_type(element, cwd, folders_dir, other_dir)

if __name__ == "__main__":
    main()


    


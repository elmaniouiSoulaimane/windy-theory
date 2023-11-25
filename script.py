#!/usr/bin/env python3
import os
import json
import argparse
from utils import organize_entry, find_dir

def main():

    #1-GET THE WANTED DISTINATION
    #must validate input
    target_name = input("Type in the name of the folder you want to organize: ")
    target_paths = find_dir(target_name)
    target_path = None

    if len(target_paths) is not 0:
        if len(target_paths) > 1:
            print(f"(i) It seems like there are multiple folders in your computer that are named \"{target_name}\".")
            print("(i) Here are the paths for each folder that I found:")
            counter = 0
            for item in target_paths:
                counter += 1
                print(f"(i) {counter}-{item}")
        
            #must validate input
            item_index = input("(i) Type the number of the wanted destination:")
            target_path = target_paths[int(item_index)-1]

        elif len(target_paths) == 1:
            target_path = target_paths[0]
        
        if os.getcwd() is not target_path:
            os.chdir(target_path)
    
        #organizing elements only if they exist
        if len(os.listdir()):
            for entry in os.listdir():
                organize_entry(entry)
    else:
        print(f"There's no folder named \"{target_name}\"")
    
    print("Done!")


if __name__ == "__main__":
    main()


    


#!/usr/bin/env python3
import os
import pyinputplus as pyip
import json
import argparse
from utils import organize, find_dir


#TO DO: must isolate tasks codes i.e components, maybe put each task in a module ?
def main():
    target_name = pyip.inputStr("(i) Type in the name of the folder you want to organize: ")
    target_paths = find_dir(target_name)

    if len(target_paths) != 0:
        if len(target_paths) > 1:
            print(f"(i) It seems like there are multiple entries in your computer that are named \"{target_name}\".")
            #asks the user to choose one destination by number, and returns chosen path from list
            target_path = pyip.inputMenu(target_paths, lettered=False, numbered=True)
            organize(target_name, target_path)

        elif len(target_paths) == 1:
            answer = pyip.inputYesNo(f"(i) I've found one destination with the name \"{target_name}\", is this the one ({target_paths[0]}) ?")
            if answer == "yes":
                target_path = target_paths[0]
                organize(target_name, target_path)
            else:
                #TO DO: ask the user if they want to do something else, but since he wanted to organize something in the beginning,
                #reprompt him to give you another name
                print("Okay, bye bye!")

    else:
        print(f"Unfortunatly I did not found any file or folder with the name \"{target_name}\"")
        #must ask the user if they want to try again
    

if __name__ == "__main__":
    main()


    


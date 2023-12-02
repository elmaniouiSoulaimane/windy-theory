import os
import time
import pyinputplus as pyip

from constants import *
from utils import get_target_dir_paths, make_dir, get_entry_type, suggest_tasks

class Organize:

    #ENTRY POINT FOR ALL ORGANIZING TASKS!
    #SHOULD I WORK WITH CLASS ATTRIBUTES?
    def __init__(self, cwd):
        self.cwd = cwd #might not need this one
        self.targets = list()
        self.organised_entries = dict()


    #TO DO: Must ask user about what type of organisation he wants
    def start(self):
        target_dir_name = pyip.inputStr("(i) Type in the name of the folder you want to organize: ")
        target_paths = get_target_dir_paths(target_dir_name)

        if len(target_paths) != 0:
            if len(target_paths) > 1:
                print(f"(i) It seems like there are multiple entries in your computer that are named \"{target_dir_name}\".")
                target_path = pyip.inputMenu(target_paths, lettered=False, numbered=True) #asks the user to choose one destination by number, and returns chosen path from list
                self.check_if_empty(target_dir_name, target_path)

            elif len(target_paths) == 1:
                answer = pyip.inputYesNo(f"(i) I've found one destination with the name \"{target_dir_name}\", is this the one ({target_paths[0]}) ?")
                
                if answer == "yes":
                    target_path = target_paths[0]
                    self.check_if_empty(target_dir_name, target_path)

                else: #reprompt him to give you another name
                    self.reprompt()

        else:
            print(f"Unfortunatly I did not found any file or folder with the name \"{target_dir_name}\"")
            self.reprompt()


    def check_if_empty(self, target_dir_name, target_path, org_type):        
        #organizing elements only if they exist
        if len(os.listdir(target_path)):
            org_type = pyip.inputMenu(["By file type", "By tag"], lettered=False, numbered=True) #asks the user to choose one destination by number, and returns chosen path from list

            for entry in os.listdir():
                organized_entry = self.execute(entry, org_type)

                if organized_entry is not None:
                    self.organised_entries.append(organized_entry)

            #only display this message if there was something to be organized to begin with
            if len(self.organised_entries):
                print(f"(i) The following entries have been organized successfully!")
                for entry in self.organised_entries:
                    print(f"{entry}")
            else:
                print(f"(i) It Looks like \"{target_dir_name}\" is already organized!")
        else:
            print(f"(i) Oops! \n")
            time.sleep(1)
            print(f"(i) Looks like the folder (\"{target_dir_name}\") you chose to organize is empty!")


    def execute(self, entry, org_type):
        source = os.path.join(os.getcwd(), entry)
        destination = self.get_destination(self, entry, org_type)
        
        os.rename(source, destination)
        return entry
    

    def get_destination(self, entry, org_type):
        if org_type == "By file type":
            destination = self.get_destination_by_type(entry)
        elif org_type == "By tag":
            destination = self.get_destination_by_tag(entry)
        
        return destination
        

    def get_destination_by_type(self, entry):
        destination = None

        if os.path.isfile(entry):
            type = get_entry_type(entry)
            if type is not None:
                type_dir = make_dir(type)
                destination = os.path.join(type_dir, entry)

        elif os.path.isdir(entry):
            folders_dir = make_dir('folders')

            #TO DO: must also check if the folder I am about to organize is not among the default user dirs
            if not any(name in entry for name in DESTINATIONS): 
                destination = os.path.join(folders_dir, entry)

        else:
            other_dir = make_dir('other')
            destination = os.path.join(other_dir, entry)
        
        return destination

    
    def get_destination_by_tag(self):
        pass

    
    def reprompt(self):
        reprompt = pyip.inputYesNo(f"Would you like organize a folder with another name ?")
        if reprompt == "yes":
            self.start()
        else:
            print("Okay, what would you like to do next ?")
            suggest_tasks()
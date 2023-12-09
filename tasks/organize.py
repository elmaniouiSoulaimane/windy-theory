import os
import time
import pyinputplus as pyip

from constants import *
from utils import get_target_dir_paths, make_dir, get_entry_type, suggest_tasks

class Organize:

    #ENTRY POINT FOR ALL ORGANIZING TASKS!
    #SHOULD I WORK WITH CLASS ATTRIBUTES?
    def __init__(self, cwd = None):
        self.organised_entries = {
            "By tag" : {
                "source": None,
                "destination": None,
                "entries": list()
            },
            "By type":{
                "source": None,
                "destination": None,
                "entries": list()
            }
        }


    def start(self):
        target_dir_name = pyip.inputStr("(i) Type in the name of the folder you want to organize: ")
        target_paths = get_target_dir_paths(target_dir_name)

        if len(target_paths) != 0:
            if len(target_paths) > 1:
                print(f"(i) It seems like there are multiple entries in your computer that are named \"{target_dir_name}\". Choose the one you're looking for:")
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


    def check_if_empty(self, target_dir_name, target_path):        
        #organizing elements only if they exist
        if len(os.listdir(target_path)):
            print("What type of organisation would you like to perform ?")
            org_type = pyip.inputMenu(["By file type", "By tag"], lettered=False, numbered=True) #asks the user to choose one destination by number, and returns chosen path from list
            self.execute(org_type, target_dir_name, target_path)

        else:
            print(f"(i) Oops! \n")
            time.sleep(1)
            print(f"(i) Looks like the folder (\"{target_dir_name}\") you chose to organize is empty!")


    def execute(self, org_type, target_dir_name, target_path):
        if org_type == "By tag":
            tag = pyip.inputStr("(i) Type in the name of the tag: ")
            self.organise_by_tag(tag, target_path)
        else:
            self.organise_by_type(target_path)
        
        #only display this message if there was something to be organized to begin with
        if len(self.organised_entries):
            print(f"(i) The following entries have been organized successfully!")
            for type in self.organised_entries:
                for entry in type["entries"]:
                    print(f"{entry}")
        else:
            print(f"(i) It Looks like \"{target_dir_name}\" is already organized!")
        

    def organise_by_type(self, target_path):
        os.chdir(target_path)

        for entry in os.listdir():
            source = os.path.join(os.getcwd(), entry)

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
            
            os.rename(source, destination)
            self.update_state("By type", source, destination, entry)

    
    def organise_by_tag(self, tag, target_path):
        os.chdir(target_path)

        for entry in os.listdir():
            if tag in entry:
                tag_dir = make_dir(tag)

                source = os.path.join(os.getcwd(), entry)
                destination = os.path.join(tag_dir, entry)

                os.rename(source, destination)
                self.update_state("By tag", source, destination, entry)
            

    def update_state(self, org_type, source, destination, entry):
        if self.organised_entries[org_type]["source"] == None:
            self.organised_entries[org_type]["source"] = source
        
        if self.organised_entries[org_type]["destination"] == destination:
            self.organised_entries[org_type]["destination"] = destination
        
        self.organised_entries[org_type]["entries"].append(entry)


    def reprompt(self):
        reprompt = pyip.inputYesNo(f"Would you like organize a folder with another name ?")
        if reprompt == "yes":
            self.start()
        else:
            print("Okay, what would you like to do next ?")
            suggest_tasks()
import os
import time
import pyinputplus as pyip
from gi.overrides.keysyms import target

from constants import *
from managers.file import FileManager
from Router import Router

class Organizer:

    target_dir_name: [str, None] = None
    target_path: [str, None] = None
    org_type: [int, None] = None

    #ENTRY POINT FOR ALL ORGANIZING TASKS!
    #SHOULD I WORK WITH CLASS ATTRIBUTES?
    def __init__(self, cwd = None):
        self.organised_entries = { #FOR HISTORY PURPOSES
            "By tag" : {
                # "source": None,
                # "destination": None,
                # "entries": list()
            },
            "By type":{
                # "source": None,
                # "destination": None,
                # "entries": list()
            }
        }


    def start(self):
        self.ask_for_target()
        self.check_if_empty()
        self.execute()

    def ask_for_target(self) -> None:
        """
        Prompts the user to input the name of the folder they want to organize and returns the target directory name and path.
        Returns:
            tuple: A tuple containing the target directory name (str) and path (str).
        """
        self.target_dir_name = pyip.inputStr("(i) Type in the name of the folder you want to organize: ")
        found_paths: list = FileManager.get_target_dir_paths(self.target_dir_name)

        if not found_paths:
            print(f"Unfortunately I did not find any file or folder with the name \"{self.target_dir_name}\"")
            self.reprompt()

        if len(found_paths) >= 1:
            print(f"(i) It seems like there are multiple entries in your computer that include the name \"{self.target_dir_name}\". Please choose the one you're looking for:")
            self.target_path : str = pyip.inputMenu(found_paths, lettered=False, numbered=True)  # asks the user to choose one destination by number, and returns chosen path from list
        
        self.target_path : str = found_paths[0]


    def check_if_empty(self):
        #organizing elements only if they exist
        if not os.listdir(self.target_path): # lists all files and directories in a specified directory path
            print(f"(i) Oops! \n")
            time.sleep(1)
            print(f"(i) Looks like the folder (\"{self.target_dir_name}\") you chose to organize is empty!")
            self.reprompt()


    def ask_for_organization_type(self):
        print("What type of organisation would you like to perform ?")
        self.org_type = pyip.inputMenu(["By file type/extension", "By a tag/name"], lettered=False, numbered=True)
        

    def execute(self):
        os.chdir(self.target_path)

        if self.org_type == 2:
            self.organise_by_tag()
        else:
            self.organise_by_type()
        
        #only display this message if there was something to be organized to begin with
        #TO DO: Must verify the values if full, because the variable already contains objects
        if len(self.organised_entries):
            print(f"(i) The following entries have been organized successfully!")
            for type in self.organised_entries:
                for entry in type['entries']:
                    print(f"{entry}")
        else:
            print(f"(i) It Looks like \"{self.target_dir_name}\" is already organized!")


    def organise_by_tag(self):
        # input must not be complex chars
        tag = pyip.inputStr("(i) Type in the name of the tag: ")

        for entry in os.listdir():
            if tag in entry:
                try: # moving the found entries to the tag directory
                    # creating a directory for the tag
                    tag_dir = FileManager.make_dir(tag)

                    source = os.path.join(os.getcwd(), entry)
                    destination = os.path.join(tag_dir, entry)

                    os.rename(source, destination)
                    self.update_state("By tag", source, destination, entry)

                except Exception as e:
                    raise e


    def organise_by_type(self):
        for entry in os.listdir():
            source = os.path.join(os.getcwd(), entry)
            destination = None

            if os.path.isfile(entry):
                entry_type = FileManager.get_entry_type(entry)

                if entry_type:
                    type_dir = FileManager.make_dir(entry_type)
                    destination = os.path.join(type_dir, entry)

            elif os.path.isdir(entry):
                folders_dir = FileManager.make_dir('folders')

                #TO DO: must also check if the folder I am about to organize is not among the default user dirs
                if not any(name in entry for name in DEFAULT_DIRS):
                    destination = os.path.join(folders_dir, entry)

            else:
                other_dir = FileManager.make_dir('other')
                destination = os.path.join(other_dir, entry)
            
            os.rename(source, destination)
            self.update_state("By type", source, destination, entry)


    def reprompt(self):
        answer = pyip.inputYesNo(f"Would you like to organize a folder with another name ?")

        if answer == "no":
            print("Okay, what would you like to do next ?")
            Router.suggest_tasks()

        else:
            self.start()


    def update_state(self, type, source, destination, entry):

        if self.organised_entries[self.org_type]["source"] == None: #TO DO: This is likely wrong, what if the key already has a value?
            self.organised_entries[self.org_type]["source"] = source
        
        if self.organised_entries[self.org_type]["destination"] == destination: #TO DO: Same here
            self.organised_entries[self.org_type]["destination"] = destination
        
        self.organised_entries[self.org_type]["entries"].append(entry)




#STANDARD LIBRARY IMPORTS
import os

#LOCAL IMPORTS
from utils import suggest_tasks

#THIRD PARTY IMPORTS
import pyinputplus as pyip


class Cleanup:
    def __init__(self):
        self.removed_empty_dirs = list()


    def start(self):
        print("What kind of cleanup would you like to perform ?")
        cleanup_type = pyip.inputMenu([
                            "Remove all empty folders in your computer",
                            "Remove duplicate files",
                            "Empty Trash", 
                            "Fresh start",
                        ], lettered=False, numbered=True)
        
        confirmation = pyip.inputYesNo(f"(i) Are you sure you want to \"{cleanup_type}\"")
            
        if confirmation == "yes":
            if cleanup_type == "Remove all empty folders in computer":
                self.rm_empty_dirs()
            elif cleanup_type == "Remove duplicate files":
                self.rm_duplicates()
            elif cleanup_type == "Empty Trash":
                self.empty_trash()
            elif cleanup_type == "Fresh start":
                self.fresh_start()
            
        else:
            self.reprompt()


    def rm_empty_dirs(self):
        #TO DO: must get user's name
        for root, dirs, files in os.walk('/home/soulaiman/', topdown=True, onerror=None, followlinks=False):
                
                for dir in dirs:
                    dir_path = os.path.join(root, dir)

                    if len(os.listdir(dir_path)) == 0:
                        os.rmdir(dir_path)
                        self.removed_empty_dirs.append(dir_path)
    

    def empty_trash(self):
        pass


    def rm_duplicates(self):
        pass


    def fresh_start(self):
        pass


    def reprompt(self):
        reprompt = pyip.inputYesNo(f"Would you like perform another cleanup action ?")
        if reprompt == "yes":
            self.start()
        else:
            print("Okay, what would you like to do next ?")
            suggest_tasks()
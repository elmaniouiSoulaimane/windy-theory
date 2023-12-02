import os
import pyinputplus as pyip


class Cleanup:
    def __init__(self):
        self.removed_empty_dirs = list()

    def start(self):
        print("What type of cleanup would you like to have ?")
        cleanup_type = pyip.inputMenu([
                            "Remove all empty folders in computer",
                            "Remove duplicate files",
                            "Empty Trash", 
                            "Fresh start",
                        ], lettered=False, numbered=True)
        
        if cleanup_type == "Remove all empty folders in computer":
            confirmation = pyip.inputYesNo(f"(i) Are you sure you want to remove all empty folders in your computer ?")
            
            if confirmation == "yes":
                self.remove_empty_dirs()
            else:
                self.reprompt()
        
        elif cleanup_type == "Remove duplicate files":
            pass

        elif cleanup_type == "Empty Trash":
            pass

        elif cleanup_type == "Fresh start":
            pass

    def remove_empty_dirs(self):
        #TO DO: must get user's name
        for root, dirs, files in os.walk('/home/soulaiman/', topdown=True, onerror=None, followlinks=False):
                
                for dir in dirs:
                    dir_path = os.path.join(root, dir)

                    if len(os.listdir(dir_path)) == 0:
                        self.removed_empty_dirs.append(dir_path)
                        os.rmdir(dir_path)
    
    def reprompt():
        pass
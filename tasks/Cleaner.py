#STANDARD LIBRARY IMPORTS
import os

from uaclient.daemon import cleanup

#LOCAL IMPORTS
from Router import Router

#THIRD PARTY IMPORTS
import pyinputplus as pyip


class Cleaner:

    @staticmethod
    def rm_empty_dirs():
        print("in rm_empty_dirs")
        user = os.environ.get('USER')

        # TO DO: CAN GO DIRECTLY TO THE DESTINATION / REVISE LINUX FILE SYSTEM
        for root, dirs, files in os.walk(f'/home/{user}/', topdown=True, onerror=None, followlinks=False):

            dirs[:] = [dir for dir in dirs if not dir.startswith('.')]

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                print(f"-Treating this dir => {dir_path}")
                """
                # Get the directory's permissions
                mode = os.stat(dir_path).st_mode
                print(f"-- mode => {mode}")

                # Check if the directory has specific permissions (e.g., write permission)
                #no | I will treat only the dirs inside the user and ignor others
                has_specific_permissions = bool(mode & stat.S_IWUSR)
                print(f"-- has_specific_permissions => {has_specific_permissions}")"""

                """if len(os.listdir(dir_path)) == 0:
                    print("emptyyy")
                    try:
                        os.rmdir(dir_path)
                    except OSError as e:
                        print(f'Error: {dir_path} : {e.strerror}')"""

    @staticmethod
    def empty_trash():
        deleted_entries = []
        entry_type = None

        user = os.environ.get('USER')
        os.chdir(f"/home/{user}/.local/share/Trash/files/")

        for entry in os.listdir():

            if os.path.isfile(entry):
                entry_type = "file"
                os.remove(entry)

            elif os.path.isdir(entry):
                tyentry_typepe = "folder"
                os.rmdir(entry)

            deleted_entries.append({
                "name": entry,
                "type": entry_type,
                "path": os.path.join(os.getcwd(), entry)
            })

        self.save(deleted_entries, os.getcwd())

    @staticmethod
    def rm_duplicates():
        pass

    @staticmethod
    def fresh_start():
        pass


    ACTIONS = {
        1: {
            "name": "Remove empty folders",
            "action": rm_empty_dirs
        },
        2: {
            "name": "Remove duplicates",
            "action": rm_duplicates
        },
        3: {
            "name": "Empty trash",
            "action": empty_trash
        },
        4: {
            "name": "Fresh start",
            "action": fresh_start
        },
    }

    def __init__(self):
        self.del_dirs = list()

    
    # def save(self, deleted_entries, source_dir):
        
    @staticmethod
    def is_hidden_dir(dir_name):
        return dir_name.startswith('.')
    

    def start(self):
        cleanup_type: int = self.get_cleanup_type()

        print(f"Performing cleanup action : {Cleaner.ACTIONS[cleanup_type]['name']}")
        Cleaner.ACTIONS[cleanup_type]["action"]()


    def get_cleanup_type(self) -> int:
        options = [action["name"] for action in Cleaner.ACTIONS.values()]

        print("What kind of cleanup would you like to perform ?")
        cleanup_type = pyip.inputMenu(options, lettered=False, numbered=True)

        confirmation = pyip.inputYesNo(f"(i) Are you sure you want to \"{cleanup_type}\"?")

        if confirmation == "no":
            self.reprompt()

        return cleanup_type


    def reprompt(self):
        reprompt = pyip.inputYesNo(f"Would you like perform another cleanup action ?")
        if reprompt == "yes":
            self.start()
        else:
            print("Okay, what would you like to do next ?")
            Router.suggest_tasks()
    
    
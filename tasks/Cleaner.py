#STANDARD LIBRARY IMPORTS
import os
import logging
import shutil

#LOCAL IMPORTS
from Router import Router

#THIRD PARTY IMPORTS
import pyinputplus as pyip


class Cleaner:

    @staticmethod
    def rm_empty_dirs():
        """
        Removes empty directories from the user's home directory.

        This method traverses the directory tree of the user's home directory,
        excluding directories that start with a dot (.), and deletes any
        directories that are found to be empty. If a directory is not empty,
        it is skipped.

        Raises:
            OSError: If an error occurs while attempting to delete a directory.
        """
        user = os.environ.get('USER')

        for root, dirs, files in os.walk(f'/home/{user}/', topdown=True, onerror=None, followlinks=False):
            
            # filters the dirs list to exclude directories that start with a dot (.)
            dirs[:] = [dir for dir in dirs if not dir.startswith('.')]

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                logging.info(f"-Treating this dir => {dir_path}")

                # Checking if the directory is empty
                if not os.path.exists(os.path.join(dir_path, '*')):
                    logging.info(f"Directory {dir_path} is empty, deleting it...")
                    
                    try:
                        shutil.rmtree(dir_path)
                        logging.info(f"Directory {dir_path} has been deleted successfully.")
                    
                    except OSError as e:
                        logging.error(f'Error while deleting {dir_path} : {e}')
                        raise OSError(f"Error while deleting {dir_path} : {e}")

                else:
                    logging.info(f"Directory {dir_path} is not empty, skipping it.")

    @staticmethod
    def empty_trash():
        """
        Empties the trash directory.

        This method empties the trash directory by deleting all entries inside it.
        If an error occurs while deleting an entry, it is logged and raised as an OSError.
        The method returns a list of entries that were deleted from the trash, including their name, type, and path.
        """
        deleted_entries = []
        entry_type = None

        user = os.environ.get('USER')
        trash_dir = f"/home/{user}/.local/share/Trash/files/"

        if not os.path.exists(trash_dir):
            logging.info(f"Trash directory does not exist: {trash_dir}")
            return

        for entry in os.listdir(trash_dir):
            entry_path = os.path.join(trash_dir, entry)

            if os.path.isfile(entry_path):
                try:
                    entry_type = "file"
                    os.remove(entry_path)
                except OSError as e:
                    logging.error(f"Error while deleting {entry_path} file from trash: " + str(e))
                    raise OSError(f"Error while deleting {entry_path} file from trash: " + str(e))

            elif os.path.isdir(entry_path):
                try:
                    entry_type = "folder"
                    os.rmdir(entry_path)
                except OSError as e:
                    logging.error(f"Error while deleting {entry_path} folder from trash: " + str(e))
                    raise OSError(f"Error while deleting {entry_path} folder from trash: " + str(e))

            deleted_entries.append({
                "name": entry,
                "type": entry_type,
                "path": entry_path
            })

    ACTIONS = {
        1: {
            "name": "Remove empty folders",
            "action": rm_empty_dirs
        },
        3: {
            "name": "Empty trash",
            "action": empty_trash
        }
    }

    def __init__(self):
        """
        Initialises the Cleaner object.
        """

    def start(self):
        """
        Starts the cleanup process.

        Asks the user for the type of cleanup to perform,
        prints a message with the type of cleanup to be performed,
        and calls the corresponding cleanup function.

        Args:
            None

        Raises:
            Exception: If the user selects an invalid cleanup type.
        """
        cleanup_type: int = self.get_cleanup_type()

        print(f"Performing cleanup action : {Cleaner.ACTIONS[cleanup_type]['name']}")
        Cleaner.ACTIONS[cleanup_type]["action"]()

    def get_cleanup_type(self) -> int:
        """
        Asks the user for the type of cleanup to perform.

        Prints a list of available cleanup actions, asks the user to select one,
        asks for confirmation, and returns the selected cleanup type as an int.

        Args:
            None

        Returns:
            int: The selected cleanup type.
        """
        options = [action["name"] for action in Cleaner.ACTIONS.values()]

        print("What kind of cleanup would you like to perform ?")
        cleanup_type = pyip.inputMenu(options, lettered=False, numbered=True)

        confirmation = pyip.inputYesNo(f"(i) Are you sure you want to \"{cleanup_type}\"?")

        if confirmation == "no":
            self.reprompt()

        return cleanup_type

    def reprompt(self):
        """
        Prompts the user to decide whether to perform another cleanup action or suggest new tasks.

        Asks the user a yes/no question about performing another cleanup action. If the user answers "yes",
        it restarts the cleanup process. If the user answers "no", it suggests other tasks to perform.
        """
        reprompt = pyip.inputYesNo("Would you like perform another cleanup action ?")
        if reprompt == "yes":
            self.start()
        else:
            print("Okay, what would you like to do next ?")
            Router.suggest_tasks()
    
    
import os
from constants import *

class FileManager:

    def __init__(self):
        pass

    @staticmethod
    def get_target_dir_paths(target_dir: str) -> list:
        """
        Returns a list of paths to directories that match the given target directory name.

        Args:
            target_dir (str): The name of the target directory.

        Returns:
            list: A list of paths to directories that match the given target directory name.
        """
        found_dirs = list()
        user = os.environ.get('USER')

        for root, dirs, files in os.walk(f'/home/{user}/', topdown=True, onerror=None, followlinks=False):

            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # TO DO: This should also check if the typed name string is found in the dir name, not just the exact name,
            # might also add the possibility to type both the name and the dir to look into
            if target_dir in dirs:
                target_dir_path = os.path.join(root, target_dir)
                found_dirs.append(target_dir_path)

        return found_dirs

    @staticmethod
    def make_dir(name):
        new_dir_path = os.path.join(os.getcwd(), name)

        if os.path.exists(new_dir_path):
            return new_dir_path
        else:
            try:
                os.mkdir(new_dir_path)
                return new_dir_path
            except OSError as error:
                print(error)
                return None

    # DON'T REMEMBER HOW THIS WORKS, MUST ASK GPT
    @staticmethod
    def get_entry_type(entry):
        for dict in FILE_TYPES_AND_EXTENSIONS:
            if any(
                    ((extension[0] in entry) or (extension[0].upper() in entry))
                    for extension in dict.get("extensions", [])):
                return dict.get("type")
        return None
import enum
import logging
import os
import time
from typing import Optional
import logging

import pyinputplus as pyip

from Router import Router
from managers.entry import EntryManager
from models import Operation
from models.entries import Entry

logger = logging.getLogger(__name__)

class OrganizationType(enum.Enum):
    BY_KEYWORD = "keyword"
    BY_EXTENSION = "extension"

    def __str__(self):
        return self.value


class Organizer:

    def __init__(self):
        """
        Initialises the Organizer object.

        The following attributes are set to None during initialization:
            - target_dir_name: The name of the target directory to organize.
            - target_path: The path of the target directory to organize.
            - org_type: The type of organization to perform (e.g. by extension, by size, etc.).
        """
        self.target_dir_name: Optional[str] = None
        self.target_path: Optional[str] = None
        self.org_type: Optional[int] = None
        
    def start(self):
        """
        Starts the organization process.

        Asks the user to select the target directory to organize,
        checks if the directory is empty,
        asks the user to select the type of organization,
        and executes the organization process based on the type of organization selected by the user.
        """
        self.ask_for_target()
        self.check_if_empty()
        self.ask_for_organization_type()
        self.execute()

    def ask_for_target(self) -> None:
        """
        Prompts the user to input the name of the folder they want to organize and returns the target directory name and path.
        Returns:
            tuple: A tuple containing the target directory name (str) and path (str).
        """
        self.target_dir_name = pyip.inputStr("(i) Type in the name of the folder you want to organize: ")
        found_paths: list = EntryManager.get_target_dir_paths(self.target_dir_name)

        if not found_paths:
            print(f"Unfortunately I did not find any file or folder with the name \"{self.target_dir_name}\"")
            self.reprompt()

        if len(found_paths) == 1:
            self.target_path: str = found_paths[0]
            return

        if len(found_paths) > 1:
            print(f"(i) It seems like there are multiple entries in your computer that include the name \"{self.target_dir_name}\". Please choose the one you're looking for:")
            self.target_path: int = pyip.inputMenu(found_paths, lettered=False, numbered=True)  # asks the user to choose one destination by number, and returns chosen path from list
            return

    def check_if_empty(self):
        """
        Checks if the target directory is empty, and if so, prompts the user to choose another directory.
        """
        if not os.listdir(self.target_path): # lists all files and directories in a specified directory path
            print("(i) Oops! \n")
            time.sleep(1)
            print(f"(i) Looks like the folder (\"{self.target_dir_name}\") you chose to organize is empty!")
            self.reprompt()

    def ask_for_organization_type(self):
        """
        Prompts the user to select the type of organization to perform on the target directory.

        Sets:
            self.org_type (int): The organization type selected by the user. 
                                1 for organizing by a keyword, 
                                2 for organizing by file extension.
        """
        print("What type of organisation would you like to perform ?")
        self.org_type = pyip.inputMenu(choices=[str(OrganizationType.BY_KEYWORD), str(OrganizationType.BY_EXTENSION)], lettered=False, numbered=True)

    def execute(self):
        """
        Executes the organization process on the target directory based on the selected organization type.

        Changes the current working directory to the target path and performs the organization by tag or by type
        depending on the value of `self.org_type`. After organizing, it displays a message with the organized entries
        if there were any changes made, otherwise it indicates that the directory was already organized.

        Raises:
            Exception: If an error occurs during the organization process.
        """
        os.chdir(self.target_path)

        if self.org_type == 1:
            self.organise_by_keyword()
        else:
            self.organise_by_extension()

    @staticmethod
    def organise_by_keyword():
        """
        Organises the entries in the target directory by a tag/name.

        Prompts the user for a tag name and moves all the entries containing that tag to a new directory with the same name.

        Args:
            None

        Raises:
            Exception: If an error occurs during the organization process.
        """
        # TODO: input value must comply with the filesystem's naming conventions
        keyword = pyip.inputStr("(i) Type-in the keyword: ")

        for entry in os.listdir():
            if os.path.isfile(entry):
                if keyword in entry:
                    try: # moving the found entries to the tag directory
                        # creating a directory for the tag
                        keyword_dir = EntryManager.make_dir(keyword)

                        origin = os.path.join(os.getcwd(), entry)
                        destination = os.path.join(keyword_dir, entry)

                        os.rename(origin, destination)
                        logger.info(f"Entry '{entry}' has been moved from '{origin}' to '{destination}'")

                        entry_type = EntryManager.get_type(entry)
                        new_entry = Entry.create(name=entry, ext=entry_type, origin=origin, destination=destination)
                        new_operation = Operation

                    except OSError as e:
                        logging.error(f"Error occurred while organizing {entry}, by {keyword} tag, details: {str(e)}")
                        raise OSError(f"Error occurred while organizing {entry}, by {keyword} tag, details: {str(e)}")

    @staticmethod
    def organise_by_extension():
        """
        Organises the entries in the target directory by type.

        Organises files by type into folders such as documents, videos, images, archives, programs, and folders.
        Also organises other entries that are not files or folders into an "other" folder.

        Args:
            None

        Raises:
            Exception: If an error occurs during the organization process.
        """
        for entry in os.listdir():
            if os.path.isfile(entry):
                entry_type = EntryManager.get_type(entry)

                if entry_type:
                    type_dir = EntryManager.make_dir(entry_type)
                    destination = os.path.join(type_dir, entry)
                else:
                    other_dir = EntryManager.make_dir('other')
                    destination = os.path.join(other_dir, entry)

                try:
                    source = os.path.join(os.getcwd(), entry)
                    os.rename(source, destination)

                    Entry.create(name=entry, ext=entry_type, origin=source, destination=destination)
                except OSError as e:
                    logging.error(f"Error occurred while organizing {entry} by {entry_type} type: {e}")
                    raise OSError(f"Error occurred while organizing {entry} by {entry_type} type: {e}")

    def reprompt(self):
        """
        Asks the user if they want to organize a folder with another name.

        Prompts the user with a yes/no question. If the user answers "no", it prints a message and suggests tasks again.
        If the user answers "yes", it starts the organization process again.
        """
        answer = pyip.inputYesNo("Would you like to organize a folder with another name ?")

        if answer == "no":
            print("Okay, what would you like to do next ?")
            Router.suggest_tasks()

        else:
            self.start()

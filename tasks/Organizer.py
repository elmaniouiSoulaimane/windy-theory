# STANDARD LIBRARY IMPORTS
from asyncio import Task
from genericpath import isdir
import os
import time
import logging
from venv import create

# THIRD PARTY IMPORTS
import pyinputplus as pyip
from typing import Optional

# LOCAL IMPORTS
from constants import DEFAULT_DIRS
from managers.file import FileManager
from Router import Router
from managers.database import DatabaseManager
from models import operations
from models.entries import Entry
from models.operations import Operation
from models.users import User
from models.tasks import Task


class Organizer:

    target_dir_name: Optional[str] = None
    target_path: Optional[str] = None
    org_type: Optional[int] = None

    def __init__(self):
        pass

    def start(self):
        """
        Starts the organization process.

        Asks the user to select the target directory to organize,
        checks if the directory is empty,
        and executes the organization process based on the type of organization selected by the user.
        """
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
                                1 for organizing by file type/extension, 
                                2 for organizing by a tag/name.
        """
        print("What type of organisation would you like to perform ?")
        self.org_type = pyip.inputMenu(["By file type/extension", "By a tag/name"], lettered=False, numbered=True)    

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

        if self.org_type == 2:
            self.organise_by_tag()
        else:
            self.organise_by_type()
        
        #only display this message if there was something to be organized to begin with
        #TO DO: Must verify the values if full, because the variable already contains objects
        if len(self.organised_entries):
            print("(i) The following entries have been organized successfully!")
            for type in self.organised_entries:
                for entry in type['entries']:
                    print(f"{entry}")
        else:
            print(f"(i) It Looks like \"{self.target_dir_name}\" is already organized!")

    def organise_by_tag(self):
        """
        Organises the entries in the target directory by a tag/name.

        Prompts the user for a tag name and moves all the entries containing that tag to a new directory with the same name.

        Args:
            None

        Raises:
            Exception: If an error occurs during the organization process.
        """
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

                except OSError as e:
                    logging.error(f"Error occurred while organizing {entry} by {tag} tag: {e}")
                    raise OSError(f"Error occurred while organizing {entry} by {tag} tag: {e}")

    def organise_by_type(self):
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
            source = os.path.join(os.getcwd(), entry)
            destination = None

            if os.path.isfile(entry):
                entry_type = FileManager.get_entry_type(entry)

                if entry_type:
                    type_dir = FileManager.make_dir(entry_type)
                    destination = os.path.join(type_dir, entry)

            elif os.path.isdir(entry):
                folders_dir = FileManager.make_dir('folders')

                if not any(name in entry for name in DEFAULT_DIRS):
                    destination = os.path.join(folders_dir, entry)

            else:
                other_dir = FileManager.make_dir('other')
                destination = os.path.join(other_dir, entry)
            
            try:
                os.rename(source, destination)
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


    @staticmethod
    def get_entry_type(entry)-> str:
        if os.path.isfile(entry):
            return "file"
        elif os.path.isdir(entry):
            return "dir"


    def save_record_in_db(self, organization_type: str, entry, origin_path:str):
        db_session = DatabaseManager.create_session()

        try:
            Organizer.create_entry_element(db_session, entry, origin_path)
            Organizer.create_operation_element(db_session, entry=entry, organization_type=organization_type)
            db_session.commit()

        except Exception as e:
            db_session.rollback()
            print(f"Error saving record: {e}")

        finally:
            db_session.close()

    @staticmethod
    def create_entry_element(session, entry, origin_path:str)-> None:
        entry_type = Organizer.get_entry_type(entry)

        entry_elm = Entry(name=entry, type=entry_type, path=origin_path)

        session.add(entry_elm)


    @staticmethod
    def create_operation_element(session, entry, organization_type)-> None:
        user_name = os.environ.get('USER')

        entry_elm = session.query(Entry).filter_by(name=entry).first()
        user = session.query(User).filter_by(name=user_name).first()
        task = session.query(Task).filter_by(name=organization_type).first()

        if not entry_elm or not user or not task:
            print(f"Missing required data: entry={entry_elm}, user={user}, task={task}")
            return

        operation = Operation(task=task, entry=entry_elm, user=user)
        
        session.add(operation)

        

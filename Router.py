import os
import time
import sqlite3
from managers.file import FileManager

from constants import *
import pyinputplus as pyip

class Router:

    @staticmethod
    def suggest_tasks():
        #LOCAL IMPORTS BECAUSE OF CIRCULAR IMPORTS
        from tasks.Organizer import Organizer
        from tasks.Cleaner import Cleaner

        new_task = pyip.inputMenu([
                                    "Organize",
                                    "Cleanup",
                                    "Backup",
                                    "Install",
                                    "Uninstall",
                                    "Undo",
                                    "History",
                                    "Help",
                                    "Quit"
                            ], lettered=False, numbered=True)

        #I need to confirm for sensitive options
        if new_task == "help":
            pass

        elif new_task == "Organize":
            task = Organizer()
            task.start()

        elif new_task == "Cleanup":
            task = Cleaner()
            task.start()

        elif new_task == "Backup":
            pass

        elif new_task == "Quit":
            pass


    """
    @staticmethod
    def setup_env():
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
    
        username = os.environ.get('USER')
    
        cursor.execute(f'SELECT * FROM users WHERE name = {username}')
    
        user = cursor.fetchone() is None:
        """
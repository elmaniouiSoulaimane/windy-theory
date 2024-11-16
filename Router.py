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
                                    "Undo",
                                    "History",
                                    "Help",
                                    "Quit"
                            ], lettered=False, numbered=True)

        if new_task == "Organize":
            task = Organizer()
            task.start()

        elif new_task == "Cleanup":
            task = Cleaner()
            task.start()
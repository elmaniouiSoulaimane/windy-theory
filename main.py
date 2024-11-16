#!/usr/bin/env python3

#LOCAL IMPORTS
from Router import Router
from managers.database import DatabaseManager

def main():

    print("Welcome to WindyTheory File Organizer! 🌪️")
    DatabaseManager()
    Router.suggest_tasks()


if __name__ == "__main__":
    main()


    


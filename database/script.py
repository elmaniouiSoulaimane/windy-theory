import sqlite3


def setup():
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS task_groups (
                id INTEGER PRIMARY KEY,
                name TEXT,
            )
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                task_group_id INTEGER,
                FOREIGN KEY (task_group_id) REFERENCES task_groups(id)
            )
        '''
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS target_dirs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            alias TEXT,
            path TEXT,
            exists INTEGER,
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            path TEXT,
        )
    ''')

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                source_dir_path TEXT,
                destination_dir_path TEXT,
                task_id INTEGER,
                entry_id INTEGER,
                FOREIGN KEY (task_id) REFERENCES tasks(id),
                FOREIGN KEY (entry_id) REFERENCES entries(id),
            )
        '''
    )

    conn.commit()
    cursor.close()
    conn.close()

def fill_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO task_groups (name) VALUES (?)', 
        ('Cleanup'),
        ('Organize'),
        ('Backup'),
        ('Install'),
        ('Uninstall'),
    )

    cursor.execute(
        'INSERT INTO tasks (name, task_group_id) VALUES (?,?)', 
        ('Remove empty folders', '1'),
        ('Remove duplicates', '1'),
        ('Empty Trash', '1'),
        ('Fresh start', '1'),
        ('Organize by tag', '2'),
        ('Organize by type', '2'),
        ('Back up a folder', '3'),
        ('Back up by type', '3'),
        ('Back up everything', '3'),
    )

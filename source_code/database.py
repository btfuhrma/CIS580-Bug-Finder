import sqlite3

def connect(db_name='app_database.db'):
    """
    Connects to the SQLite database. If the database does not exist, it creates one.
    Returns a connection object.
    """
    connection = sqlite3.connect(db_name)
    print(f"Connected to the database: {db_name}")
    return connection

def create_table():
    """
    Creates a user table if it doesn't exist.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    print("User table created.")
    conn.close()

def save_to_db(username, password, email):
    """
    Saves a new user to the database.
    """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (username, password, email))
        conn.commit()
        print(f"User '{username}' saved to database.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")
    finally:
        conn.close()

def get_user(username):
    """
    Retrieves user information from the database.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

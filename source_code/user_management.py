from database import save_to_db, get_user

def login(username, password):
    """
    Authenticates a user based on username and password.
    """
    user = get_user(username)
    if user:
        if user[2] == password:  # Assuming user[2] is the password
            print(f"User '{username}' logged in successfully.")
            return True
        else:
            print("Incorrect password.")
            return False
    else:
        print("User not found.")
        return False

def logout(username):
    """
    Logs out the user and confirms the action.
    """
    print(f"User '{username}' logged out.")

def register(username, password, email):
    """
    Registers a new user.
    """
    if len(password) < 6:
        print("Password must be at least 6 characters long.")
        return False

    save_to_db(username, password, email)
    print(f"User '{username}' registered successfully.")
    return True

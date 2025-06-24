from database import database
from app.auth import is_master_password_set, setup_master_password, verify_master_password
from app.logic import load_master_key  
from app.gui.main_window import run_app

def main():
    database.initialize_database()

    if not is_master_password_set():
        password = input("Set a master password: ")
        master_key = setup_master_password(password)
    else:

        for _ in range(3):
            password = input("Enter master password: ")
            master_key = verify_master_password(password)
            if master_key:
                break
            print("Incorrect password, try again.")
        else:
            print("Too many failed attempts. Exiting.")
            return

    run_app(master_key)

if __name__ == "__main__":
    main()




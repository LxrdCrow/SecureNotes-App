from database import database  
from app import logic          

def main():
    print("🚀 Starting Secure Notes...")

    database.initialize_database()

    logic.load_master_key()

    print("✅ Secure Notes ready to use!")

if __name__ == "__main__":
    main()

from db_setup import initialize_db
from admin import add_question, import_questions_from_csv, view_users, block_user
from quiz import take_quiz
from leaderboard import show_leaderboard

def login():
    username = input("Username: ")
    password = input("Password: ")

    import sqlite3
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT role, status FROM login WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()

    if result:
        role, status = result
        if status == 'blocked':
            print("Your account is blocked.")
            return None, None
        return username, role
    else:
        print("Invalid credentials.")
        return None, None

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Question")
        print("2. Import Questions from CSV")
        print("3. View Users")
        print("4. Block User")
        print("5. View Leaderboard")
        print("6. Logout")
        choice = input("Enter choice: ")

        if choice == '1':
            add_question()
        elif choice == '2':
            import_questions_from_csv()
        elif choice == '3':
            view_users()
        elif choice == '4':
            username = input("Enter username to block: ")
            block_user(username)
        elif choice == '5':
            show_leaderboard()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def user_menu(username):
    while True:
        print("\nUser Menu:")
        print("1. Take Quiz")
        print("2. View Leaderboard")
        print("3. Logout")
        choice = input("Enter choice: ")

        if choice == '1':
            take_quiz(username)
        elif choice == '2':
            show_leaderboard()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    initialize_db()
    print("Welcome to the Quiz Management System!")
    while True:
        username, role = login()
        if role == 'admin':
            admin_menu()
        elif role == 'user':
            user_menu(username)
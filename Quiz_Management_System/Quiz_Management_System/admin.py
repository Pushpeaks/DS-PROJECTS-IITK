import sqlite3
import csv

def add_question():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    question = input("Enter question: ")
    options = [input(f"Option {i+1}: ") for i in range(4)]
    answer = input("Enter correct option (1-4): ")
    c.execute("INSERT INTO quiz VALUES (?, ?, ?, ?, ?, ?)", (question, *options, answer))
    conn.commit()
    conn.close()
    print("Question added successfully.")

def import_questions_from_csv(filename='quiz.csv'):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 6:
                c.execute("INSERT INTO quiz VALUES (?, ?, ?, ?, ?, ?)", tuple(row))
    conn.commit()
    conn.close()
    print("Questions imported from CSV.")

def view_users():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    for row in c.execute("SELECT username, role, status FROM login"):
        print(row)
    conn.close()

def block_user(username):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("UPDATE login SET status='blocked' WHERE username=?", (username,))
    conn.commit()
    conn.close()
    print(f"User '{username}' has been blocked.")
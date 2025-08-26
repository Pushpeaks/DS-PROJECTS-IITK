import sqlite3

def initialize_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()

    # Create login table
    c.execute('''CREATE TABLE IF NOT EXISTS login (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT,
                    status TEXT)''')

    # Create quiz table
    c.execute('''CREATE TABLE IF NOT EXISTS quiz (
                    question TEXT,
                    option1 TEXT,
                    option2 TEXT,
                    option3 TEXT,
                    option4 TEXT,
                    answer TEXT)''')

    # Create leaderboard table
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                    username TEXT,
                    score INTEGER)''')

    # Insert default users
    c.execute("INSERT OR IGNORE INTO login VALUES ('admin', 'admin123', 'admin', 'active')")
    c.execute("INSERT OR IGNORE INTO login VALUES ('user1', 'user123', 'user', 'active')")

    conn.commit()
    conn.close()
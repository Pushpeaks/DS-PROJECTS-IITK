import sqlite3

def show_leaderboard():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    print("\nLeaderboard:")
    for row in c.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10"):
        print(f"{row[0]}: {row[1]}")
    conn.close()
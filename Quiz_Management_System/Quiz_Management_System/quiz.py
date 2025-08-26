import sqlite3

def take_quiz(username):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    questions = c.execute("SELECT * FROM quiz").fetchall()
    score = 0

    for q in questions:
        print(f"\n{q[0]}")
        for i in range(1, 5):
            print(f"{i}. {q[i]}")
        ans = input("Your answer (1-4): ")
        if ans == q[5]:
            score += 1

    print(f"\nQuiz completed! Your score: {score}/{len(questions)}")
    c.execute("INSERT INTO leaderboard VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()
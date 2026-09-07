import sqlite3
import os

print("DB script started")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "interview_coach.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS admin(
id INTEGER PRIMARY KEY AUTOINCREMENT,
questions TEXT,
answer TEXT,
job_role TEXT,
subject TEXT,
hints TEXT,
keypoints TEXT,
difficulty TEXT
)
''')

conn.commit()
conn.close()

print("DB created successfully")

cur.execute('''
CREATE TABLE login_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    logout_time DATETIME,
    ip_address TEXT,
    device TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')


cur.execute('''
CREATE TABLE interview_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    session_number INTEGER,
    job_role TEXT,
    total_questions INTEGER,
    answered_questions INTEGER DEFAULT 0,
    overall_percentage REAL DEFAULT 0,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cur.execute('''
CREATE TABLE session_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_number INTEGER,
    username TEXT,
    question_id INTEGER,
    user_answer TEXT,
    percentage REAL
)
''')


conn.commit()
conn.close()

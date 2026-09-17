import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "interview_coach.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS interview_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    session_number INTEGER,
    job_role TEXT,
    total_questions INTEGER,
    answered_questions INTEGER DEFAULT 0,
    overall_percentage REAL DEFAULT 0,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS session_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_number INTEGER,
    username TEXT,
    question_id INTEGER,
    user_answer TEXT,
    percentage REAL
)
""")

conn.commit()
conn.close()

print("Tables created successfully!")


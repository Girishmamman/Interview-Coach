from flask import Flask, app, render_template, request, redirect, url_for, session
from evaluate import analyze_answer
import sqlite3
import os

# DATABASE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "interview_coach.db")


# HOME PAGE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')
    

# =========================
# LOGIN PAGE
# =========================


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['admin'] = username
            return redirect(url_for('admin'))

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))

        else:
            return render_template(
                'login.html',
                error ="Invalid Username or Password"
            )

    return render_template('login.html')

# SIGNUP PAGE

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template(
                "signup.html",
                error="Passwords do not match"
            )

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()

        if user:
            conn.close()
            return render_template(
                "signup.html",
                error="Username already exists"
            )

        cur.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        session['username'] = username

        return redirect(url_for('dashboard'))

    return render_template("signup.html")

#admin page

@app.route('/admin')
def admin():
    return render_template('admin.html')

# VIEW ADMIN QUESTIONS
# =========================
@app.route('/view_admin')
def view_admin():

    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM admin")
    records = cur.fetchall()

    conn.close()

    return render_template('view_admin.html', records=records)


# =========================
# SAVE QUESTION (ADMIN)
# =========================
@app.route('/save_question', methods=['POST'])
def save_question():

    question = request.form['question']
    answer = request.form['answer']
    job_role = request.form['job_role']
    subject = request.form['subject']
    hints = request.form['hints']
    keypoints = request.form['keypoints']
    difficulty = request.form['difficulty']

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO admin
        (questions, answer, job_role, subject, hints, keypoints, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer,
        job_role,
        subject,
        hints,
        keypoints,
        difficulty
    ))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

@app.route('/clear_admin')
def clear_admin():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Delete all records
    cur.execute("DELETE FROM admin")

    # Reset the AUTOINCREMENT counter
    cur.execute("DELETE FROM sqlite_sequence WHERE name='admin'")

    conn.commit()
    conn.close()

    return redirect(url_for('view_admin'))

@app.route('/Edit/<int:id>', methods=['GET', 'POST'])
def Edit(id):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":

        cur.execute("""
        UPDATE admin
        SET questions=?, answer=?, job_role=?, subject=?,
            hints=?, keypoints=?, difficulty=?
        WHERE id=?
        """, (

            request.form["questions"],
            request.form["answer"],
            request.form["job_role"],
            request.form["subject"],
            request.form["hints"],
            request.form["keypoints"],
            request.form["difficulty"],
            id

        ))

        conn.commit()
        conn.close()

        return redirect(url_for("view_admin"))

    question = cur.execute(
        "SELECT * FROM admin WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("Edit.html", question = question)

@app.route('/Delete/<int:id>')
def Delete(id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM admin WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('view_admin'))

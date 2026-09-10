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



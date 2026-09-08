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
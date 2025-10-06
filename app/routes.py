from flask import render_template , redirect , url_for , flash 
from app import app

@app.route('/')
def homepage():
    return render_template('homepage.html')
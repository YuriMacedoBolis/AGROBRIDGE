from flask import render_template , redirect , url_for , flash 
from flask_login import login_user , login_required , logout_user
from app import app , db , bcrypt
from app.forms import *

@app.route('/')
def homepage():
    return render_template('homepage.html')


#LOGIN
@app.route('/login', methods=["GET" , "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nome = form.nome.data).first()
        if user and bcrypt.check_password_hash(user.password_hash , form.password.data):
            login_user(user)
            return redirect(url_for('homepage'))
    return render_template('login.html' , form = form)


#REGISTRAR
@app.route('/register', methods=["GET" , "POST"])
def registrar():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nome = form.nome.data ,email = form.email.data ,password_hash = hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('homepage'))
    
    return render_template('register.html' , form=form)

#SOBRE NOS
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


        

from flask import render_template , redirect , url_for , flash 
from flask_login import login_user , login_required , logout_user
from app import app , db , bcrypt , google
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


#LOGIN COM GOOGLE
@app.route('/login/google')
def login_google():
    try:
        app.logger.info('Iniciando login com google')
        redirect_uri = url_for('authorize_google' , _external=True)
        app.logger.info(f'redirect URI: {redirect_uri}')
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f'Erro durante login:{str(e)}')
        return redirect(url_for('login'))
    
    

@app.route('/authorize/google')
def authorize_google():
    try:
        token = google.authorize_access_token() 
    except Exception as e:
        flash(f'Erro na autorização do Google: {str(e)}', 'danger')
        app.logger.error(f'Erro ao obter token de acesso: {str(e)}')
        return redirect(url_for('login'))

    user_info = token.get('userinfo')
    
    if not user_info:
        userinfo_endpoint = google.server_metadata['userinfo_endpoint']
        resp = google.get(userinfo_endpoint)
        resp.raise_for_status() 
        user_info = resp.json()

    email = user_info.get('email')
    display_name = user_info.get('name', email)
    
    user = User.query.filter_by(email=email).first()

    if not user:        
        base_nome = display_name.replace(" ", "").lower() 
        base_nome = base_nome[:90] # Garante que o nome não exceda o limite de 100
        
        nome_final = base_nome
        counter = 1
        while User.query.filter_by(nome=nome_final).first():
            nome_final = f"{base_nome[:90-len(str(counter))]}{counter}"
            counter += 1
        
        # O nome de usuário criado agora é garantidamente ÚNICO no banco
        nome_para_db = nome_final
        # -----------------------------------------------------------------

        user = User(nome=nome_para_db, email=email, password_hash='google_oauth')
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            # Em caso de falha rara, rollback e informa o erro
            db.session.rollback()
            flash('Não foi possível registrar o novo usuário devido a um erro no banco de dados.', 'danger')
            app.logger.error(f'Falha ao commitar novo usuário do Google: {str(e)}')
            return redirect(url_for('login'))

    login_user(user)
    flash(f'Login com Google bem-sucedido, bem-vindo(a) {user.nome}!', 'success')
    return redirect(url_for('homepage'))

        

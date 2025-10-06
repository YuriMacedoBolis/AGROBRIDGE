from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired  , EqualTo , ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    nome = StringField("Nome de usuário:" , validators=[DataRequired()])
    email = StringField("Email:" , validators=[DataRequired()])
    password = PasswordField("Senha:" , validators=[DataRequired()])
    confirm_password = PasswordField("Confirme sua Senha:" ,validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField("Registrar")
    
    def validate_username(self , nome):
        user = User.query.filter_by(nome=nome.data).first()
        if user:
            raise ValidationError("Este nome de usuário já está em uso. Por Favor escohla outro")
        
class LoginForm(FlaskForm):
    nome = StringField("Nome de usuário:" , validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Senha:" , validators=[DataRequired()])
    submit = SubmitField("Login")
from app import db , login_manager
from flask_login import UserMixin

class User(db.Model , UserMixin):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer , primary_key = True)
    nome = db.Column(db.String(100) , unique=True , nullable = False)
    email = db.Column(db.String(100) , unique=True , nullable = False)
    password_hash = db.Column(db.String(200) , nullable=True)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
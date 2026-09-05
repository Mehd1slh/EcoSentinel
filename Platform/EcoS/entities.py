from sqlalchemy.orm import relationship
from dataclasses import dataclass
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime, timezone , timedelta
from EcoS import db , login_manager ,app
from flask_login import UserMixin
from fpdf import FPDF

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_current_date():
    return datetime.now(timezone.utc)+ timedelta(hours=1)



class User(db.Model , UserMixin):

    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) , unique=True , nullable=False)
    email = db.Column(db.String(50) , unique=True , nullable=False)
    mdp = db.Column(db.String(255) , nullable=False)
    img = db.Column(db.String(255) , nullable=False , default = 'default.jpg')
    privilege = db.Column(db.String(15) , nullable=False , default = 'user')
    acd = db.Column(db.DateTime, nullable=False, default=get_current_date)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.img}')"
    


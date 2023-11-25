import random
import os
import base64
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cocktails = db.relationship('Cocktail', backref='author')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password', ''))

    def __repr__(self):
        return f"<User {self.id}|{self.username}"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(days=1)
        db.session.commit()
        return self.token
    
@login.user_loader
def get_user(user_id):
    return db.session.get(User, user_id)



class Cocktail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String, nullable=False)
    glass_type = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructions = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    drink_type = db.Column(db.Boolean, nullable=False)
    ingredient_1 = db.Column(db.String, nullable=False)
    measure_1 = db.Column(db.String, nullable=False)
    ingredient_2 = db.Column(db.String, nullable=False)
    measure_2 = db.Column(db.String, nullable=False)
    ingredient_3 = db.Column(db.String)
    measure_3 = db.Column(db.String)
    ingredient_4 = db.Column(db.String)
    measure_4 = db.Column(db.String)
    ingredient_5 = db.Column(db.String)
    measure_5 = db.Column(db.String)
    ingredient_6 = db.Column(db.String)
    measure_6 = db.Column(db.String)
    ingredient_7 = db.Column(db.String)
    measure_7 = db.Column(db.String)
    ingredient_8 = db.Column(db.String)
    measure_8 = db.Column(db.String)
    ingredient_9 = db.Column(db.String)
    measure_9 = db.Column(db.String)
    ingredient_10 = db.Column(db.String)
    measure_10 = db.Column(db.String)

    def __repr__(self):
        return f"<Cocktail{self.id}|{self.drink_name}>"

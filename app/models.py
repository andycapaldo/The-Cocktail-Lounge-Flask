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
    cocktails = db.relationship('Cocktail', backref='author', cascade='all, delete')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='author', passive_deletes=True, cascade='all, delete')

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
        self.token_expiration = now + timedelta(days=365)
        db.session.commit()
        return self.token
    
    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'username': self.username
        }
    
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
    comments = db.relationship('Comment', backref='cocktail', passive_deletes=True, cascade='all, delete')

    def __repr__(self):
        return f"<Cocktail{self.id}|{self.drink_name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'drinkName': self.drink_name,
            'glassType': self.glass_type,
            'dateCreated': self.date_created,
            'author': self.author.to_dict(),
            'instructions': self.instructions,
            'imageUrl': self.image_url,
            'drinkType': self.drink_type,
            'ingredient1': self.ingredient_1,
            'measure1': self.measure_1,
            'ingredient2': self.ingredient_2,
            'measure2': self.measure_2,
            'ingredient3': self.ingredient_3,
            'measure3': self.measure_3,
            'ingredient4': self.ingredient_4,
            'measure4': self.measure_4,
            'ingredient5': self.ingredient_5,
            'measure5': self.measure_5,
            'ingredient6': self.ingredient_6,
            'measure6': self.measure_6,
            'ingredient7': self.ingredient_7,
            'measure7': self.measure_7,
            'ingredient8': self.ingredient_8,
            'measure8': self.measure_8,
            'ingredient9': self.ingredient_9,
            'measure9': self.measure_9,
            'ingredient10': self.ingredient_10,
            'measure10': self.measure_10,
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Comment{self.id}|{self.cocktail_id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "dateCreated": self.date_created,
            "author": self.author.to_dict() if self.author else None,
            "cocktail": self.cocktail.to_dict() if self.cocktail else None
        }
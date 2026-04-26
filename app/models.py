
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    decks      = db.relationship('Deck', backref='owner')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Deck(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_public   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards       = db.relationship('Card', backref='deck', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Deck {self.title}>'

class Card(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer   = db.Column(db.Text, nullable=False)
    deck_id  = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.question[:30]}>'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
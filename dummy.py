from flask_sqlalchemy import SQLAlchemy
from app.app import Kanban_app
from app.models import db, User, Card
from passlib.hash import sha256_crypt
import hashlib

# created tables if not already created
db.create_all()

password_1 = "12345"
hash_p_1 = sha256_crypt.hash(password_1)

# create dummy accounts
dummy_users = [
    User("test@gmail.com",
    hash_p_1),
]

db.session.add_all(dummy_users)
db.session.commit()

# create dummy kanban cards
dummy_cards = [
    Card(1,
    0,
    "Breakfast",
    "Remember to eat it"),
    Card(1,
    2,
    "Groceries",
    "Buy eggs")
]

db.session.add_all(dummy_cards)
db.session.commit()

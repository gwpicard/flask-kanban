from flask_sqlalchemy import SQLAlchemy
from app.app import Kanban_app

db = SQLAlchemy(Kanban_app)

# User class
class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    # return userid
    def get_userid(self):
        return self.userid

    # add methods to match flask-login requirements
    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

# card class for Kanban
class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    status = db.Column(db.Integer) # whether to-do, in progress, or done
    header = db.Column(db.String(80))
    desc = db.Column(db.String(120))

    def __init__(self, userid, status, header, desc):
        self.userid = userid
        self.status = status
        self.header= header
        self.desc = desc

from flask import Flask, request, render_template, redirect, url_for, flash
from app.forms import SignupForm
from passlib.hash import sha256_crypt
import json

Kanban_app = Flask(__name__)

Kanban_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
Kanban_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/kanban.db'
Kanban_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.models import db, User, Card
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(Kanban_app)
login_manager.login_view = "login"
login_manager.refresh_view = "login"
login_manager.session_protection = "strong"

@Kanban_app.route('/')
@login_required
def index():
    # retrieve current userid from flask_login current_user
    userid = current_user.get_userid()
    # get all cards stored under userid
    cards = Card.query.filter_by(userid=userid).all()

    return render_template('index.html', cards=cards)

@Kanban_app.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('signup.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():

            # search if email already exists
            if User.query.filter_by(email=form.email.data).first():
                error = "Email address already exists"
                return render_template('signup.html', form=form, error=error)

            # create user if user does not exist in database
            else:
                password = form.password.data
                # safely store hashed password
                hash_password = sha256_crypt.encrypt(password)
                newuser = User(form.email.data, hash_password)
                db.session.add(newuser)
                db.session.commit()

                flash('Thanks for registering!')
                return redirect(url_for('login'))

        # if form doesn't validate
        else:
            error = "Form didn't validate"
            return render_template('signup.html', form=form, error=error)

@Kanban_app.route('/login', methods=['GET','POST'])
def login():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            # find user in database
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                # hash password
                password = form.password.data
                # verify password against hash
                if sha256_crypt.verify(password, user.password):

                    # log user into app session
                    login_user(user)

                    return redirect(url_for('index'))

                # if password does not match hash
                else:
                    error = "Wrong password"
                    return render_template('login.html', form=form, error=error)
            # user does not exist in database
            else:
                error = "User doesn't exist. Please sign up"
                return render_template('login.html', form=form, error=error)
        # if form doesn't validate
        else:
            error = "Form didn't validate"
            return render_template('login.html', form=form, error=error)

# delete card
@Kanban_app.route("/delete", methods=['POST'])
@login_required
def delete():
    # create session to add and commit to
    s = db.session()

    card_id = int(request.data)

    s.query(Card).filter_by(id=card_id).delete()

    # commit deletion to database
    s.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# save all cards
@Kanban_app.route("/save", methods=['POST'])
@login_required
def save():
    # create session to add and commit to
    s = db.session()
    # get current userid
    userid = current_user.get_userid()

    new_cards = []

    for card in request.json:
        # retrieve card ID from JSON post request
        card_id = card["ID"]
        status = int(card["status"])
        header = card["header"]
        desc = card["desc"]

        # update card if already in database
        if card_id != "N" and card_id != "added":
            card_id = int(card_id)
            update_card = s.query(Card).filter_by(id=card_id).one()
            update_card.status = status
            update_card.header = header
            update_card.desc = desc

        # prevent new card from being added twice to database
        elif card_id == "added":
            pass

        # else add new card
        else:
            # add to list to be committed
            new_cards.append(Card(userid, status, header,desc))

    # commit any remaining session objects to database
    s.add_all(new_cards)
    s.commit()
    # return 200 if saving is successful
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@Kanban_app.route("/logout")
@login_required
def logout():
    logout_user() # logout use using flask-login
    return redirect(url_for('login'))

################################################################################

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()

# Initialise database function
def init_db():
    db.init_app(Kanban_app)
    db.app = Kanban_app
    db.create_all() # create models in model.py

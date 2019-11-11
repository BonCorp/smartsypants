import os
import functools
from flask import Flask, render_template, session, request, redirect, flash, g
from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, MetaData, DateTime, func
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# its dangerous package to handle passwords and such
from itsdangerous import URLSafeTimedSerializer

from flask_session import Session

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))

metadata = MetaData()

# API key and secret
api_key = "m2yuVbMZPhY2Es41AhbA"
secret = "uZux5gULwA97zc9cDRPkD4tS4yj0l7ZHJKOc5B05Fk"


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    username = session.get('username')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute('SELECT * FROM users WHERE id= :id', {"id": user_id}).fetchone()
        print(f"current user is {g.user}")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("login")
        return view(**kwargs)

    return wrapped_view()


@app.route("/")
def index():
    print(session.get('user_id'))
    return render_template('index.html')


@app.route("/register", methods=("GET", "POST"))
def register():
    """Register user"""
    # User reached route via post
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password_hash']
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute('SELECT * FROM users WHERE username = :username',
                        {"username": username}).fetchone() is not None:
            error = 'Username {} is already taken. Choose another name.'.format(username)
        if error is None:
            db.execute('INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)',
                       {"username": username, "password_hash": generate_password_hash(password)})

            db.commit()
            return redirect("/")
        flash(error)
    return render_template("register.html")


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.execute('SELECT * FROM users WHERE username = :username', {"username": username}).fetchone()

        if user is None:
            error = "Username Incorrect"
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            print(f"username is {user[1]}")
            return redirect('/')
        flash(error)
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


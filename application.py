import os

from flask import Flask, render_template, session
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker

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

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String, nullable=False, unique=True),
              Column('password', String, nullable=False),
              Column('first_name', String(20)),
              Column('last_name', String(20)),
              Column('avatar_url', String))


metadata.create_all(engine)

# API key and secret
api_key = "m2yuVbMZPhY2Es41AhbA"
secret = "uZux5gULwA97zc9cDRPkD4tS4yj0l7ZHJKOc5B05Fk"


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
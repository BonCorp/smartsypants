import csv
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, func
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))

metadata = MetaData()

# creates tables

# create book table
books = Table('books', metadata,
              Column('id', Integer, primary_key=True),
              Column('isbn', String, unique=True),
              Column('title', String),
              Column('author', String),
              Column('year', String)
              )

# create user table
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(20), unique=True, nullable=False),
              Column('password_hash', String(128), nullable=False)
              )

reviews = Table('reviews', metadata,
                Column('id', Integer, primary_key=True),
                Column('text', String, nullable=False),
                Column('books_id', ForeignKey('books.id'), nullable=False),
                Column('user_id', ForeignKey('users.id'), nullable=False),
                Column('created_date', DateTime(timezone=True), server_default=func.now())

                )

metadata.create_all(engine)

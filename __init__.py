from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(os.getcwd(),"blog.db3")
app.config['SECRET_KEY']=os.urandom(32)
db = SQLAlchemy(app)
db.create_all()
from blog import app
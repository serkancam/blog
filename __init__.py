from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os

app=Flask(__name__)
ckeditor=CKEditor()

app.config['CKEDITOR_PKG_TYPE'] = 'full-all'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(os.getcwd(),"blog.db3")
app.config['SECRET_KEY']=os.urandom(32)
ckeditor.init_app(app)
db = SQLAlchemy(app)
db.create_all()
from blog import app
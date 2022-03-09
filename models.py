from blog import db

#db sınıfları
class User(db.Model):
    __tablename__ = 'user'   
    username = db.Column(db.String(80) , primary_key=True)
    email=db.Column(db.String(80))
    password = db.Column(db.String(255))
    permission = db.Column(db.Integer)
    articles = db.relationship('Article', backref='user', lazy='dynamic')  
   
class Article(db.Model):
    __tablename__ = 'article'    
    time = db.Column(db.DateTime,primary_key=True)    
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    username = db.Column(db.String(80),db.ForeignKey('user.username'), nullable=False)    
    image_path = db.Column(db.String(255))
    tags = db.relationship('Article_Tag', backref='article', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tag'
    name = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.String(80))
    articles = db.relationship('Article_Tag', backref='tag', lazy='dynamic')
   
class Article_Tag(db.Model):
    __tablename__ = 'article_tag'
    time = db.Column(db.DateTime, db.ForeignKey('article.time'), primary_key=True)
    tag_name = db.Column(db.String(30), db.ForeignKey('tag.name'),primary_key=True)
   

#db sınıfları
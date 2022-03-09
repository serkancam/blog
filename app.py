from flask import flash,render_template,Response,request,redirect,url_for,session,logging
from passlib.hash import sha256_crypt
from blog import app,db
from blog.forms import RegisterForm,LoginForm,ArticleAddForm
from blog.models import User,Tag,Article,Article_Tag
from functools import wraps
from datetime import datetime
from math import ceil
import os
from werkzeug.utils import secure_filename

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function
# Kullanıcı Giriş Decorator'ı
# etiket listesi getir
def get_tags():    
    tags = db.session.query(Tag.name,db.func.count(Article_Tag.tag_name).label("count")).join(Article_Tag,Tag.name==Article_Tag.tag_name,isouter=True).group_by(Tag.name).all()
    return tags
# etiket listesi getir
@app.route("/",methods=["GET","POST"])
def index():
    tags=get_tags()
    articles = db.session.query(Article).order_by(Article.time.desc()).all()
    article_tags=db.session.query(Article_Tag).all()  
    page_count=ceil(len(articles)/5)
    p=request.args.get("p",1,type=int)
    articles=articles[(p-1)*5:p*5]
      
    return render_template("index.html",tags=tags,articles=articles,article_tags=article_tags,page_count=page_count,p=p)

@app.route("/test")
def test(): 
    return render_template("test.html")


@app.route("/register",methods=["GET","POST"])
def register():
    
    form = RegisterForm(request.form)
    # form.yetki.choices=[(kullanici.email,kullanici.username) for kullanici in User.query.all()]#[(kullanici.email,kullanici.username) for kullanici in User.query.all()]    
    if request.method == "POST" and form.validate():       
        username=form.username.data
        password=sha256_crypt.encrypt(form.password.data)
        email = form.email.data
        yeniKayit=User(username=username,email=email,password=password,permission=0)
        try:
            db.session.add(yeniKayit)
            db.session.commit()
            flash("Kayıt Başarılı","success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Bu Kullanıcı Adı Zaten Kullanılıyor veya kayıt hatası","danger")
            return redirect(url_for("register"))
            
    else:
        return render_template("register.html",form = form)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method=="POST":        
        name = request.form['username']
        passw = request.form['password']        
        bilgi=User.query.filter_by(username=name).first()       
        if bilgi is not None:
            g_passw=bilgi.password
            if sha256_crypt.verify(passw,g_passw):
                session['logged_in'] = True
                session['username']=name
                
                return redirect(url_for("index"))
            else:
                return render_template("login.html",form = form,durum="parolanızı kontrol ediniz")               
        
        else:       
            

            return render_template("login.html",form = form,durum="Böyle bir kullanıcı yok")
    else:
        return render_template("login.html",form = form,durum="")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/admin/article_add",methods=["GET","POST"])
@login_required
def article_add():
    
    form = ArticleAddForm(request.form)
    
    form.tags.choices=[(tag.name,tag.name) for tag in Tag.query.all()]#[(kullanici.email,kullanici.username) for kullanici in User.query.all()]
    
    if request.method == "POST" and form.validate() and len(form.tags.data)>0:   
        time=datetime.utcnow()
        title=form.title.data
        content=form.content.data
        username=session['username']
        image_path=""
       
        try:
            image_data = request.files[form.image.name]         
            if image_data.filename != "":             
                filename = secure_filename(image_data.filename)
                image_path=app.config["IMAGE_UPLOADS"]+filename
                image_data.save(image_path)               
            else:
                image_path="static/img/python.png"   
            
              
            db.session.add(Article(time=time,title=title,content=content,username=username,image_path=image_path))
            for tag in form.tags.data:
                db.session.add(Article_Tag(time=time,tag_name=tag))
            db.session.commit()
            form=ArticleAddForm()
            form.tags.choices=[(tag.name,tag.name) for tag in Tag.query.all()]
            
            return render_template("article_add.html",form =form,durum="Kayıt eklendi")      
                
        except Exception as e:
            
            return render_template("article_add.html",form = form,durum="Hata oluştu"+str(e))     
    else:   
        return render_template("article_add.html",form = form,durum="")


@app.route("/article",methods=["GET","POST"])
def article():
    q=request.args.get("q")
    article=Article.query.filter_by(time=q).first()
    article_tags=Article_Tag.query.filter_by(time=q).all()
    
    return render_template("article.html",article=article,article_tags=article_tags,tags=get_tags())


@app.route("/articles/<tag>",methods=["GET","POST"])
def tags_articles(tag):
    tags=get_tags()
    articles = db.session.query(Article).join(Article_Tag, Article.time==Article_Tag.time).filter(Article_Tag.tag_name==tag).order_by(Article.time.desc()).all()
    article_tags=db.session.query(Article_Tag).all()  
      
    return render_template("index.html",tags=tags,articles=articles,article_tags=article_tags)
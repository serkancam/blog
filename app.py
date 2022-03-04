from flask import Flask,flash,render_template,Response,request,redirect,url_for,session,logging
from passlib.hash import sha256_crypt
from blog import app,db
from blog.forms import RegisterForm,LoginForm,ArticleAddForm
from blog.models import User,Tag,Article,Article_Tag
from functools import wraps
from datetime import datetime
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
@app.route("/",methods=["GET","POST"])
def index():
    a=request.args.get("a")
      
    return render_template("index.html")

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
                flash("Başarıyla Giriş Yaptınız...","success")
                return redirect(url_for("index"))
            else:
                flash("Parolanızı Yanlış Girdiniz...","danger")
                return redirect(url_for("login"))                 
        
        else:           
            

            flash("Böyle bir kullanıcı bulunmuyor...","danger")
            
            return redirect(url_for("login"))
     
   
    return render_template("login.html",form = form)


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


@app.route("/article_add",methods=["GET","POST"])
@login_required
def article_add():
    
    form = ArticleAddForm(request.form)
    form.tags.choices=[(tag.name,tag.name) for tag in Tag.query.all()]#[(kullanici.email,kullanici.username) for kullanici in User.query.all()]
    
    if request.method == "POST" and form.validate():   
        time=datetime.utcnow()
        title=form.title.data
        content=form.content.data
        username=session['username']
        try:
            db.session.add(Article(time=time,title=title,content=content,username=username))
            for tag in form.tags.data:
                db.session.add(Article_Tag(time=time,tag_name=tag))
            db.session.commit()
            return render_template("article_add.html",form = form,durum="Kayıt eklendi")      
                
        except Exception as e:
            
            return render_template("article_add.html",form = form,durum="Hata oluştu"+str(e))     
    else:   
        return render_template("article_add.html",form = form,durum="")
    
         
        # username=form.username.data
        # password=sha256_crypt.encrypt(form.password.data)
        # email = form.email.data
        # yeniKayit=Article(username=username,email=email,password=password,permission=0)
        # try:
        #     db.session.add(yeniKayit)
        #     db.session.commit()
        #     flash("Kayıt Başarılı","success")
        #     return redirect(url_for("index"))
        # except Exception as e:
        #     flash("Bu Kullanıcı Adı Zaten Kullanılıyor veya kayıt hatası","danger")
        #     return redirect(url_for("article_add"))
  
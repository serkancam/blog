from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField,DateField,IntegerField,SubmitField,SelectMultipleField,widgets
from  flask_ckeditor import CKEditorField


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
# Kullanıcı Kayıt Formu
class RegisterForm(Form):   
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola:",validators=[validators.DataRequired(message = "Lütfen bir parola belirleyin")])
    confirm = PasswordField("Parola Doğrula",validators=[validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")])    
    submit = SubmitField("Kayıt ol")
# Kullanıcı Kayıt Formu
#login formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı",validators=[validators.DataRequired(message = "Lütfen kullanıcı adınızı giriniz...")])
    password = PasswordField("Parola",validators=[validators.DataRequired(message = "Lütfen parolanızı giriniz...")])
    submit = SubmitField(label="Giriş")
#login formu

class ArticleAddForm(Form):  
    title = StringField("Yazı başlığı",validators=[validators.Length(min = 5,max = 50),validators.DataRequired(message = "Lütfen bir başlık giriniz...")])
    content = CKEditorField("İçerik",validators=[validators.DataRequired(message = "Lütfen bir yazı girin...")])
    tags=MultiCheckboxField("Etiketler",choices=[])     
    submit = SubmitField("Kayıt")
# Kullanıcı Kayıt Formu

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms.validators import DataRequired
from passlib.context import CryptContext
import time


### DEFAULT_ENVIROMENT_SETTING_UP
class MyForm(FlaskForm):
    recaptcha = RecaptchaField()

## FLASK_WTF_SETTING_UP
## FLASK_SETTING_UP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SECRET_KEY'] = 'GarfieldIsHandsome'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeiQsIUAAAAAC6CBe8ooH-dGTQbHrB0XEWjFeSz"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LeiQsIUAAAAAMXsKvlwUCy5VfrYUcayO5THXX6j"
db = SQLAlchemy(app)

## FLASK_LOGIN_SETTING_UP

login_manager = LoginManager(app)


## OTHER_SETTING_UP
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    created_on = db.Column(db.Integer, nullable=False)
    updated_on = db.Column(db.Integer, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Integer, nullable=False)
    updated_on = db.Column(db.Integer, nullable=False)

    def encrypt_password(self, password):
        self.password = pwd_context.encrypt(password)

    def check_encrypted_password(self, hashed):
        return pwd_context.verify(self.password, hashed)

### FUNCTIONAL

## FUNCTIONS

def encrypt_password(password):
    return pwd_context.encrypt(password)


## FLASK ROUTES

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("views/index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        result = User.query.filter(User.email == request.form['email']).first()
        if result:
            if result.check_encrypted_password(encrypt_password(request.form['password'])):
                login_user(result)
                flash("Success!")
            else:
                flash("Bad password, please try again!")
        else:
            flash("Email address not exist!")
    elif request.method == "GET":
        if not current_user.is_authenticated:
            return render_template("views/login.html", form=MyForm())
        else:
            return redirect(url_for("home"))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        print(request.form)
        result = User.query.filter(User.email == request.form['email']).first()
        if not result:
            try:
                newUser = User(first_name = request.form['firstname'],\
                               last_name = request.form['lastname'],\
                               email = request.form['email'],\
                               password = request.form['password'],\
                               created_on = int(time.time()),\
                               updated_on = int(time.time()))
                db.session.add(newUser)
            except:
                db.session.roll_back()
                flash("Bad input, please try again!")
                return redirect(url_for('signup'))
            else:
                db.session.commit()
                flash('Successful registed!')
                return redirect(url_for('login'))
        else:
            flash("Areally have account on this email.")
    elif request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    return render_template("views/signup.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

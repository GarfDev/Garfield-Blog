from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = 'GarfieldIsHandsome'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    created_on = db.Column(db.Integer, nullable=False)
    updated_on = db.Column(db.Integer, nullable=False)




@app.route('/', methods=['GET','POST']) ## specify route with methods
def home():
    return "Hello"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

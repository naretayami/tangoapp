from flask import Flask,render_template,request,session,redirect,url_for
from models.models import List, User
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256

import spacy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.secret_key = key.SECRET_KEY


@app.route("/")
def top():    
    return render_template("top.html") 


@app.route("/login")
def login():
    status = request.args.get("status")
    return render_template("login.html",status=status)


@app.route("/authentication",methods=["post"])
def authentication():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login",status="wrong_password"))
    else:
        return redirect(url_for("login",status="user_notfound"))


@app.route("/signup")
def signup():
    status = request.args.get("status")
    return render_template("signup.html",status=status)


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("signup",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("login",status="logout"))


@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        return render_template("index.html",name=name)
    else:
        return redirect(url_for("login",status="logout"))


@app.route('/new')
def new():
    if "user_name" in session:
        name = session["user_name"]
        return render_template("new.html",name=name)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/add",methods=["post"])
def add():
    if "user_name" in session:
        userid = session["user_name"] 
        front = request.form["front"]
        back = request.form["back"]
        doc = nlp(request.form["front"])
        for token in doc:
            partofspeech = token.pos_ 
        memo = request.form["memo"]
        count = 0
        content = List(userid,front,back,partofspeech,memo,count,datetime.today())
        db_session.add(content)
        db_session.commit()
        return redirect(url_for("index"))



@app.route("/studying")
def studying():
    if "user_name" in session:
        name = session["user_name"]
        studyALL = List.query.filter_by(userid=name)
        return render_template("studying.html",studyALL=studyALL)
    else:
        return redirect(url_for("/",status="logout"))


if __name__ == "__main__":
    app.run(debug=True)
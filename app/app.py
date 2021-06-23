from flask import Flask,render_template,request,session,redirect,url_for
from models.models import List, User
from models.database import db_session
from datetime import datetime
from datetime import timedelta
from app import key
from hashlib import sha256
import spacy


app = Flask(__name__)
app.secret_key = key.SECRET_KEY


nlp = spacy.load("en_core_web_sm")


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
            part_to_speech = token.pos_
    
            if part_to_speech == 'VERB':
                partofspeech = '動詞'
            elif part_to_speech == 'NOUN':
                partofspeech = '名詞'
            elif part_to_speech == 'ADJ':
                partofspeech = '形容詞'
            elif part_to_speech == 'ADP':
                partofspeech = '前置詞'
            elif part_to_speech == 'ADV':
                partofspeech = '副詞'
            elif part_to_speech == 'AUX':
                partofspeech = '助動詞'
            elif part_to_speech == 'CONJ':
                partofspeech = '接続詞'
            elif part_to_speech == 'CCONJ':
                partofspeech = '等位接続詞'
            elif part_to_speech == 'DET':
                partofspeech = '限定詞'
            elif part_to_speech == 'INTJ':
                partofspeech = '間投詞、感嘆詞'
            elif part_to_speech == 'NUM':
                partofspeech = '数詞'
            elif part_to_speech == 'PART':
                partofspeech = '助詞'
            elif part_to_speech == 'PRON':
                partofspeech = '代名詞'
            elif part_to_speech == 'PROPN':
                partofspeech = '固有名詞'
            elif part_to_speech == 'PUNCT':
                partofspeech = '句読点'
            elif part_to_speech == 'SCONJ':
                partofspeech = '従属接続詞'
            elif part_to_speech == 'SYM':
                partofspeech = 'シンボル'
            elif part_to_speech == 'X':
                partofspeech = '他' 
            elif part_to_speech == 'SPACE':
                partofspeech = '空白'        
            else:
                partofspeech = part_to_speech 
        memo = request.form["memo"]
        sumcount = 0
        count = 0
        content = List(userid,front,back,partofspeech,memo,sumcount,count,datetime.today())
        db_session.add(content)
        db_session.commit()
        return redirect(url_for("index"))


@app.route("/studying")
def studying():
    if "user_name" in session:
        name = session["user_name"]
        studyALL = List.query.filter_by(userid=name).order_by(List.date.asc())
        nowdate = datetime.today()
        meg = "もうちょっとこうだったら使いやすいのに、を集めた英単語アプリです。"
        meg2 = "主な機能を紹介します。"
        meg3 = "１・反復学習"
        return render_template("studying.html",studyALL=studyALL,nowdate=nowdate,meg=meg,meg2=meg2,meg3=meg3)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/allstudying")
def allstudying():
    if "user_name" in session:
        name = session["user_name"]
        studyALL = List.query.filter_by(userid=name).order_by(List.date.asc())
        return render_template("allstudying.html",studyALL=studyALL)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/complete")
def complete():
    if "user_name" in session:
        name = session["user_name"]
        studyALL = List.query.filter_by(userid=name).order_by(List.date.asc())
        return render_template("complete.html",studyALL=studyALL)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/edit/<int:id>/")
def edit(id):
    if "user_name" in session:
        study = List.query.get(id)
        return render_template("edit.html",id=id,study=study)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/update/<int:id>",methods=["post"])
def update(id):
    content = List.query.filter_by(id=id).first()
    content.back = request.form["back"]
    content.memo = request.form["memo"]
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/pronounce/<int:id>/")
def pronounce(id):
    if "user_name" in session:
        study = List.query.get(id)
        return render_template("pronounce.html",id=id,study=study)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/understand/<int:id>",methods=["post"])
def understand(id):
    content = List.query.filter_by(id=id).first()
    content.sumcount += 1
    content.count += 1
    if content.count == 1:
        content.date = datetime.today() + timedelta(minutes=1)
    elif content.count == 2:
        content.date = datetime.today() + timedelta(minutes=3)
    elif content.count == 3:
        content.date = datetime.today() + timedelta(minutes=5)
    elif content.count == 4:
        content.date = datetime.today() + timedelta(minutes=7)
    elif content.count == 5:
        content.date = datetime.today() + timedelta(minutes=14)
    elif content.count == 6:
        content.date = datetime.today() + timedelta(minutes=30)
    else:
        content.date = datetime.today()
    db_session.commit()
    return redirect(url_for("studying"))


@app.route("/repeats/<int:id>",methods=["post"])
def repeats(id):
    content = List.query.filter_by(id=id).first()
    content.sumcount += 1
    content.count = 0
    content.date = datetime.today() + timedelta(minutes=-1)
    db_session.commit()
    return redirect(url_for("studying"))


@app.route("/repeats_complete/<int:id>",methods=["post"])
def repeats_complete(id):
    content = List.query.filter_by(id=id).first()
    content.sumcount += 1
    content.count = 0
    content.date = datetime.today() + timedelta(minutes=-1)
    db_session.commit()
    return redirect(url_for("complete"))


@app.route("/repeats_allstudying/<int:id>",methods=["post"])
def repeats_allstudying(id):
    content = List.query.filter_by(id=id).first()
    content.sumcount += 1
    content.count = 0
    content.date = datetime.today() + timedelta(minutes=-1)
    db_session.commit()
    return redirect(url_for("allstudying"))


@app.route("/delete/<int:id>",methods=["post"])
def delete(id):
    id_list = request.form.getlist("delete")
    content = List.query.filter_by(id=id).first()
    db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/aimaisearch",methods=["post"])
def aimaisearch():
    if "user_name" in session:
        name = session["user_name"]
        search_word = request.form["search_word"]
        searchALL = List.query.filter_by(userid=name).filter(List.front.like('%\\' + search_word + '%', escape='\\')).all()
        if searchALL == "":
            searchresult = "お探しの英単語は登録されていません"
            return render_template("index.html",name=name,searchresult=searchresult)
        return render_template("index.html",name=name,searchALL=searchALL)
    else:
        return redirect(url_for("top",status="logout"))


@app.route("/zensearch",methods=["post"])
def zensearch():
    if "user_name" in session:
        name = session["user_name"]
        search_word = request.form["search_word"]
        searchALL = List.query.filter_by(userid=name,front=search_word).all()
        if searchALL == None:
            searchresult = 'お探しの英単語は登録されていません'
            return render_template("index.html",name=name,searchresult=searchresult)
        return render_template("index.html",name=name,searchALL=searchALL)
    else:
        return redirect(url_for("top",status="logout"))


if __name__ == "__main__":
    app.run(debug=True)

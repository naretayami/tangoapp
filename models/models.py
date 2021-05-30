from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    userid = Column(String(128))
    front = Column(String(128))
    back = Column(String(128))
    partofspeech = Column(Text)
    memo = Column(Text)
    count = Column(Integer)
    date = Column(DateTime, default=datetime.today())

    def __init__(self, userid=None, front=None, back=None, partofspeech=None, memo=None, count=None, date=None):
        self.userid = userid
        self.front = front
        self.back = back
        self.partofspeech = partofspeech
        self.memo = memo
        self.count = count
        self.date = date
        
    def __repr__(self):
       return '<front %r>' % (self.front)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)
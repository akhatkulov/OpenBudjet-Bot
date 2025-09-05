from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, func,VARCHAR,desc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from conf import DB_URL
engine = create_engine(DB_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user_openbudjet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(BigInteger, unique=True)
    step = Column(VARCHAR(25), default=0)
    money = Column(Integer,default=0)
    cache = Column(String,default="")

class Numbers(Base):
    __tablename__ = 'numbers_openbudjet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(VARCHAR(25), unique=True)


class PollingNumbers(Base):
    __tablename__ = 'polling_numbers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(VARCHAR(25), unique=True)


class Channels(Base):
    __tablename__ = 'channels_openbudjet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, default="None", unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_all_user():
    session = Session()
    try:
        x = session.query(User.cid).all()
        res = [i[0] for i in x]
        return res
    finally:
        session.close()

def user_count():
    session = Session()
    try:
        x = session.query(func.count(User.id)).first()
        return x[0]
    finally:
        session.close()

def create_user(cid,name):
    session = Session()
    try:
        user = User(cid=int(cid), step="0", money=0)
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def get_members():
    session = Session()
    try:
        x = session.query(User).where(User.cid >= 0).all()
        return x
    finally:
        session.close()
 

def check_number(number):
    session = Session()
    try:
        x = Numbers(number=number)
        session.add(x)
        session.commit()
        return True 
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()


def add_polling_number(number):
    session = Session()
    try:
        x = PollingNumbers(number=number)
        session.add(x)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()


def set_cache(cid,cache):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        x.cache = cache
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

def get_cache(cid):

    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        return x.cache if x else None
    finally:
        session.close() 

def get_money(cid):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        return x.money if x else 0
    finally:
        session.close()

def add_money(cid,payment_money):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        if x:
            res = x.money + payment_money
            x.money = res 
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

def claim_money(cid):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        if x:
            x.money = 0
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

def get_step(cid):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        return x.step if x else None
    finally:
        session.close()

def put_step(cid, step):
    session = Session()
    try:
        x = session.query(User).filter_by(cid=cid).first()
        if x:
            x.step = str(step)
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()


def put_channel(channel: str):
    session = Session()
    try:
        x = Channels(link=channel)
        session.add(x)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

def get_channel():
    session = Session()
    try:
        x = session.query(Channels).all()
        res = [i.link for i in x]
        return res
    finally:
        session.close()

def get_channel_with_id():
    session = Session()
    try:
        x = session.query(Channels).all()
        res = ""
        for channel in x:
            res += f"\nID: {channel.id} \nLink: @{channel.link}"
        return res
    finally:
        session.close()

def delete_channel(ch_id):
    session = Session()
    try:
        x = session.query(Channels).filter_by(id=int(ch_id)).first()
        if x:
            session.delete(x)
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

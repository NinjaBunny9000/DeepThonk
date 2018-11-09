from db_declarative import HaveYouEver, Users, Twitch, Base
from sqlalchemy import create_engine, desc

import random


engine = create_engine('sqlite:///db_test.sqlite')

Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind=engine)
session = DBSession()

def rand_hye():
    rows = session.query(HaveYouEver).count()
    rand_num = random.randrange(0, rows)
    rand_item = session.query(HaveYouEver).get(rand_num)
    return rand_item

def get_latest_id():
    last_id = session.query(Users).order_by(desc(Users.agnostic_id)).first()
    return last_id.agnostic_id

def get_user():
    return session.query(Twitch).get(1)


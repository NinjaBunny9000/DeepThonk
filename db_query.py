from db_declarative import HaveYouEver, Users, Twitch, Task, Base
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

def rand_task():    #TODO - Currently copy/pased HYE code
    rows = session.query(Task).count()
    rand_num = random.randrange(1, rows+1)
    rand_item = session.query(Task).get(rand_num)
    return rand_item
    
def get_latest_task():
    return session.query(Task).order_by(desc(Task.date_registered)).first()

def get_latest_id():
    last_id = session.query(Users).order_by(desc(Users.agnostic_id)).first()
    return last_id.agnostic_id

def get_user():
    return session.query(Twitch).get(1)

def get_agnostic_id_twitch(snowflake):
    temp_holder = session.query(Twitch).filter_by(snowflake=snowflake).first()
    if temp_holder is not None:
        return temp_holder.agnostic_id
    else:
        return None

def is_bot_mod(queried_agnostic_id):
    user_queried = session.query(Users).filter_by(agnostic_id=queried_agnostic_id).first()
    return user_queried.bot_mod

def is_bot_mod_twitch(name):
    user_queried = session.query(Twitch).filter_by(username=name).first()
    if user_queried is None:
        return False

    return is_bot_mod(user_queried.agnostic_id)

def set_bot_mod_twitch(name, value):
    twitch_user = session.query(Twitch).filter_by(username=name).first()
    if twitch_user is None:
        return '{} must register first!'.format(name)
    twitch_user.user.bot_mod = value
    session.commit() 
    if value:
        return '{} is now a Bot Mod.'.format(name)
    else:
        return '{} is no longer a Bot Mod.'.format(name)
        
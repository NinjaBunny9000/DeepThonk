from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db_query
from datetime import datetime
 
# DON'T FORGET to add new tables to this import..
from db_declarative import HaveYouEver, Users, Twitch, Discord, Task, Base

engine = create_engine('sqlite:///db_test.sqlite')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Session = sessionmaker(bind=engine)
# Session.configure(bind=engine)
# session = Session()


def add_user_twitch(message):
    '''Insert an agnostic user id into the User table'''
    # new_agnostic_user = Users(
    #     bot_mod=False
    # )message.author.id
    # session.add(new_agnostic_user)
    temp_holder = session.query(Twitch).filter_by(snowflake=message.author.id).first()
    if temp_holder is not None:
        return False
    # if (len(session.query(Twitch).filter(Twitch.snowflake == message.author.id)).all() > 0):
    #     return

    session.add(Users(
        # bot_mod=False,
        
        ))
    session.commit()


    new_twitch_user = Twitch(
        agnostic_id=db_query.get_latest_id(),
        snowflake=message.author.id,
        username=message.author.name
    )
    print(new_twitch_user)
   
    session.add(new_twitch_user)
    session.commit()
    return True


def add_hye(list_item, submitter):
    '''Insert an item in the HaveYouEver table'''
    new_item = HaveYouEver(
        item=list_item, 
        twitch_submitter=submitter
        )
    session.add(new_item)
    session.commit()

def add_task(description):
    '''Insert an item in the Task table'''
    new_item = Task(
        description=description
        )
    session.add(new_item)
    session.commit()
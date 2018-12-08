import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import *
from datetime import datetime

Base = declarative_base()

class Twitch(Base):
    __tablename__ = 'twitch'

    id = Column(Integer, primary_key=True)
    agnostic_id = Column(Integer, ForeignKey('users.agnostic_id'), nullable=False)
    snowflake = Column(Integer, nullable=True)
    username = Column(String(16), nullable=False)
    user = relationship("Users", back_populates="twitch")


class Discord(Base):
    __tablename__ = 'discord'

    snowflake = Column(Integer, primary_key=True)
    agnostic_id = Column(Integer, ForeignKey('users.agnostic_id'), nullable=False)
    # this will need to be updated/changed by mods manually??
    # username = Column(String(16), nullable=False)


class HaveYouEver(Base):
    __tablename__ = 'have_you_ever'

    id = Column(Integer, primary_key=True)
    item = Column(String(250), nullable=False)
    service = Column(String(15), nullable=False)
    quoter_agnostic_id = Column(Integer, ForeignKey('users.agnostic_id'), nullable=False)
    submitter_agnostic_id = Column(Integer, ForeignKey('users.agnostic_id'), nullable=False)


class BandNames(Base):
    __tablename__ = 'band_names'

    id = Column(Integer, primary_key=True)
    band_name = Column(String(250), nullable=False)
    submitter_id = Column(Integer, ForeignKey('users.agnostic_id'), nullable=False)


class Users(Base):
    __tablename__ = 'users'

    agnostic_id = Column(Integer, primary_key=True)
    bot_mod = Column(Boolean, default=0)
    date_registered = Column(DateTime, default=datetime.utcnow, nullable=True)



Users.twitch = relationship("Twitsch", order_by=Twitch.agnostic_id, back_populates="user")
Users.discord = relationship("Discord", order_by=Discord.agnostic_id, back_populates="user")

engine = create_engine('sqlite:///db_test.sqlite')

Base.metadata.create_all(engine)
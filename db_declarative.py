import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import *

Base = declarative_base()


class HaveYouEver(Base):
    __tablename__ = 'have_you_ever'

    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    item = Column(String(250), nullable=False)
    twitch_submitter = Column(String(16))

    def __repr__(self):
        return("<HaveYouEver(id={}, item={}, submitter={})>".format(
                self.id, self.item, self.twitch_submitter
            ))

engine = create_engine('sqlite:///db_test.sqlite')


Base.metadata.create_all(engine)
""" 
This class defines the models for interacting with the 10stars database
in  ORM/CRUD using Flask-SQLAlchemy.

  db.session
    Create 
      <create Model> Model(var1 = val1, var2 = val2, ...)

      .add(Model)

      <commit>

    Read
      .get(Model, primary_key_value)

      .execute(db.select(multple columns).filter_by(conditions))

      .scalars(db.select(Model or single column).filter_by(conditions))

      <use .first() if you only expect one result>

    Update
      <get a Model from the db>

      <update the Model object's attributes>

      <commit>

    Delete
      <get a Model from the db>

      .delete(Modal)
      
      <commit>

  <Commit>
    db.session.commit()

Bulk / Multi Row INSERT, upsert, UPDATE and DELETE are also available
https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#bulk-multi-row-insert-upsert-update-and-delete

More Comprehensive Docs
https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#

:author: Steven Knaack
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import List, Optional
from datetime import date, time
import os
from dotenv import load_dotenv

##### Set up #####

load_dotenv() # add variables to the environment

sql_url: str = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(
    user = os.getenv('DB_USER'), 
    password = os.getenv('DB_PASSWORD'), 
    host = os.getenv('DB_HOST'),
    port = os.getenv('DB_PORT'), 
    database = os.getenv('DB_NAME')
    )

def configure_flask_sqlalchemy(app: Flask) -> SQLAlchemy :
    """
        Configures app for Flask-SQLAlchemy and creates 
            SQLAlchemy object for use in the app
        Side-effects
            sets app.config['SQLALCHEMY_DATABASE_URI']
            sets app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    """
    db = SQLAlchemy(model_class=Base)

    # configure the MYSQL database, relative to the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize the app with the extension
    db.init_app(app)

    # return db
    return db

###### Below are the Models #######

class Base(DeclarativeBase):
  """ Base for Models """
  pass

# Sync Base's metadata with the current db
engine = create_engine(sql_url)
Base.metadata.reflect(engine)

# table `in_team` relationship representation
user_team_channel = Base.metadata.tables['in_team']

# table `participates_in` relationship representation
user_event_channel = Base.metadata.tables['participates_in']

class Membership(Base) :
    """ 
    Association object modeling many-to-many relationship between
    User and Group with the added context of Membership.role, provided
    by the `in_group` table.
    """
    __table__ = Base.metadata.tables['in_group']

    # define column properties
    user_email: Mapped[str] = __table__.columns['user_email']
    group_id: Mapped[str] = __table__.columns['group_id']
    role: Mapped[str] = __table__.columns['role']

    # define relationship properties
    user: Mapped['User'] =\
        relationship('User', back_populates='memberships')
    group: Mapped['Group'] =\
        relationship('Group', back_populates='memberships')

    # methods
    def __init__(self, user_email: str, group_id: int, role: str = 'invitee') -> None:
        """ role must be in ['invitee', 'participant', 'admin', 'owner'] """
        self.user_email = user_email
        self.group_id = group_id
        self.role = role

    def __repr__(self) -> str :
        return f'Membership(user_email: {self.user_email}; group_id: {self.group_id})>'
    
class User(Base) :
    """ Model of the `user` table. """
    __table__ = Base.metadata.tables['user']
    #__tablename__ = Base.metadata.tables['user']
    

    # define column properties
    email: Mapped[str] = __table__.columns['email']
    username: Mapped[str] = __table__.columns['username']
    password: Mapped[str] = __table__.columns['password']
    #email: Mapped[str] = db.mapped_column(db.String(255), primary_key=True)
    #username: Mapped[str] = db.mapped_column(db.String(255))
    #password: Mapped[str] = db.mapped_column(db.String(255))

    # define relationship properties
    availability_blocks: Mapped[List['AvailabilityBlock']] =\
        relationship('AvailabilityBlock', back_populates='user')
    memberships: Mapped[List['Membership']] =\
        relationship('Membership', back_populates='user')
    teams: Mapped[List['Team']] =\
        relationship('Team', secondary=user_team_channel, back_populates='members')
    events: Mapped[List['Event']] =\
        relationship('Event', secondary=user_event_channel, back_populates='participants')

    # methods
    def __init__(self, email: str, username: str, password: str) -> None :
        self.email = email
        self.username = username
        self.password = password
    
    def __repr__(self) -> str :
        return f'User(name: {self.username}; email: {self.email})'
  
class AvailabilityBlock(Base) :
    """ Model of the `availability_block` table. """
    __table__ = Base.metadata.tables['availability_block']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    start_day: Mapped[str] = __table__.columns['start_day']
    end_day: Mapped[str] = __table__.columns['end_day']
    start_time: Mapped[time] = __table__.columns['start_time']
    end_time: Mapped[time] = __table__.columns['end_time']
    user_email: Mapped[str] = __table__.columns['user_email']

    # define relationship properties
    user: Mapped['User'] =\
        relationship('User', back_populates='availability_blocks')
    
    # methods
    def __init__(self, id: int, start_day: str, end_day: str, 
                 start_time: time, end_time: time, user_email: str) -> None :
        """ 
        start_day and end_day must be in 
            ['sunday', 'monday', 'tuesday', 
            'wednesday', 'thursday', 'friday', 'saturday']
        """
        self.id = id
        self.start_day = start_day
        self.end_day = end_day
        self.start_time = start_time
        self.end_time = end_time
        self.user_email = user_email
    
    def __repr__(self) -> str :
        return f'AvailabilityBlock(id: {self.id})'
  
class Group(Base) :
    """ Model of the `group` table. """
    __table__ = Base.metadata.tables['group']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
          __table__.columns['description']

    # define relationship properties
    teams: Mapped[List['Team']] =\
        relationship('Team', back_populates='group')
    all_events: Mapped[List['Event']] =\
        relationship('Event', back_populates='group')
    memberships: Mapped[List['Membership']] =\
        relationship('Membership', back_populates='group')
 
    # methods
    def get_group_level_events(self) -> List['Event'] :
        """ Returns a List of just the group-level events """
        group_level_events: List['Event'] = []

        for event in self.all_events :
            # filter out group level events
            if event.team_id is None :
                group_level_events.append(event)

        return group_level_events
    
    def __init__(self, name: str = 'Unnamed Group', description: str = None) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str :
        return f'Group(id: {self.id}; name: {self.name})'
  
class Team(Base) :
    """ Model of the `team` table. """
    __table__ = Base.metadata.tables['team']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
        __table__.columns['description']
    group_id: Mapped[int] = __table__.columns['group_id']

    # define relationship properties
    group: Mapped['Group'] =\
        relationship('Group', back_populates='teams')
    events: Mapped[List['Event']] =\
        relationship('Event', back_populates='team')
    members: Mapped[List['User']] =\
        relationship('User', secondary=user_team_channel, back_populates='teams')
    
    # methods
    def __init__(self, id: int, 
                 name: str = 'Unnamed Team', description: str = None) -> None :
        self.id = id
        self.name = name
        self.description = description
    
    def __repr__(self) -> str :
        return f'Team(id: {self.id}; name: {self.name})'
  
class Event(Base) :
    """ Model of the `Event` table. """
    __table__ = Base.metadata.tables['event']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
        __table__.columns['description']
    start_date: Mapped[date] = __table__.columns['start_date']
    end_date: Mapped[date] = __table__.columns['end_date']
    reg_start_day: Mapped[Optional[str]] =\
        __table__.columns['reg_start_day']
    reg_end_day: Mapped[Optional[str]] =\
        __table__.columns['reg_end_day']
    start_time: Mapped[time] = __table__.columns['start_time']
    end_time: Mapped[time] = __table__.columns['end_time']
    edit_permission: Mapped[str] = __table__.columns['edit_permission']
    group_id: Mapped[int] = __table__.columns['group_id']
    team_id: Mapped[Optional[int]] = __table__.columns['team_id']

    # define relationship properties
    group: Mapped['Group'] =\
        relationship('Group', back_populates='all_events', overlaps="events")
    team: Mapped['Team'] =\
        relationship('Team', back_populates='events', overlaps='all_events,group')
    participants: Mapped[List['User']] =\
        relationship('User', secondary=user_event_channel, back_populates='events')
    
    # methods
    def is_recurring(self) -> bool :
        """ Returns true only if this event repeats weekly """
        return not self.reg_start_day and not self.reg_end_day

    def __init__(self, start_date: date, end_date: date, 
                 start_time: time, end_time: time, group_id: int,
                 team_id: int = None, name: str = 'Unnamed Event',
                 description: str = None, reg_start_day: str = None,
                 reg_end_day: str = None, edit_permission: str = 'group_admin') -> None :
        """ 
        Note edit_permission must be in 
            ['member', 'group_admin']
        and if defined reg_start_day and reg_end_day must be in 
            ['sunday', 'monday', 'tuesday', 
            'wednesday', 'thursday', 'friday', 'saturday']
        """
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.reg_start_day = reg_start_day
        self.reg_end_day = reg_end_day
        self.start_time = start_time
        self.end_time = end_time
        self.edit_permission = edit_permission
        self.group_id = group_id
        self.team_id = team_id

    def __repr__(self) -> str :
        return f'Group(id: {self.id}; name: {self.name})'
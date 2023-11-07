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
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import os
from dotenv import load_dotenv
#from pprint import pprint

##### Set up #####

load_dotenv() # add variables to the environment

#TODO create an association object membership

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# configure the MYSQL database, relative to the app instance folder
sql_url = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(
    user = os.getenv('DB_USER'), 
    password = os.getenv('DB_PASSWORD'), 
    host = os.getenv('DB_HOST'),
    port = os.getenv('DB_PORT'), 
    database = os.getenv('DB_NAME')
)

app.config['SQLALCHEMY_DATABASE_URI'] = sql_url

# initialize the app with the extension
db.init_app(app)

engine = create_engine(sql_url)
Base.metadata.reflect(engine)

###### Below are the Models #######

user_team_channel = db.metadata.tables['in_team']

user_event_channel = db.metadata.tables['participates_in']

class Membership(Base) :
    __table__ = Base.metadata.tables['in_group']

    user_email = __table__.columns['user_email']
    group_id = __table__.columns['group_id']
    role = __table__.columns['role']

    user = relationship('User', back_populates = 'memberships')
    group = relationship('Group', back_populates = 'memberships')

    def __repr__(self) :
        return f'Membership(user_email: {self.user_email}; group_id: {self.group_id})'

class User(Base) :
    __table__ = Base.metadata.tables['user']

    email = __table__.columns['email']
    username = __table__.columns['username']
    password = __table__.columns['password']

    availability_blocks = relationship('AvailabilityBlock', back_populates='user')
    
    memberships = relationship('Membership', back_populates = 'user')
    teams = relationship('Team', secondary = user_team_channel, back_populates = 'members')
    events = relationship('Event', secondary = user_event_channel, back_populates = 'participants')

    group_roles = association_proxy('groups', 'role')
    
    def __repr__(self) :
        return f'User(name: {self.username}; email: {self.email})'
  
class AvailabilityBlock(Base) :
    __table__ = Base.metadata.tables['availability_block']

    id = __table__.columns['id']
    start_day = __table__.columns['start_day']
    end_day = __table__.columns['end_day']
    start_time = __table__.columns['start_time']
    end_time = __table__.columns['end_time']

    user_email = __table__.columns['user_email']
    user = relationship('User', back_populates = 'availability_blocks')
    
    def __repr__(self) :
        return f'AvailabilityBlock(id: {self.id})'
  
class Group(Base) :
    __table__ = Base.metadata.tables['group']

    id = __table__.columns['id']
    name = __table__.columns['name']
    description = __table__.columns['description']

    teams = relationship('Team', back_populates='group')
    all_events = relationship('Event', back_populates='group')
    memberships = relationship('Membership', back_populates = 'group')
    
    def __repr__(self) :
        return f'Group(id: {self.id}; name: {self.name})'
  
class Team(Base) :
    __table__ = Base.metadata.tables['team']

    id = __table__.columns['id']
    name = __table__.columns['name']
    description = __table__.columns['description']

    group_id = __table__.columns['group_id']
    group = relationship('Group', back_populates='teams')

    events = relationship('Event', back_populates='team')

    members = relationship('User', secondary = user_team_channel, back_populates = 'teams')
    
    def __repr__(self) :
        return f'Team(id: {self.id}; name: {self.name})'
  
class Event(Base) :
    __table__ = Base.metadata.tables['event']

    id = __table__.columns['id']
    name = __table__.columns['name']
    description = __table__.columns['description']
    end_date = __table__.columns['end_date']
    reg_start_day = __table__.columns['reg_start_day']
    reg_end_day = __table__.columns['reg_end_day']
    start_time = __table__.columns['start_time']
    end_time = __table__.columns['end_time']
    edit_permission = __table__.columns['edit_permission']

    group_id = __table__.columns['group_id']
    group = relationship('Group', back_populates='all_events')

    
    team_id = __table__.columns['team_id']
    team = relationship('Team', back_populates='events')

    participants = relationship('User', secondary = user_event_channel, back_populates = 'events')
    
    def __repr__(self) :
        return f'Group(id: {self.id}; name: {self.name})'

    

####### TESTING ########
@app.route('/')
def user_table () :
    query_str = ''
    for row in db.session.scalars(db.select(Group)):
        query_str += str(row) + ' '
    return query_str

@app.route('/pop') 
def test_user_group_conn () :
    steven = db.session.get(User, 'Steven@gmail.com')
    steven.groups.append(Group(name = "Steven", description = "Steven"))
    db.session.commit()
    return str(steven.group_roles)

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('FLASK_PORT'))
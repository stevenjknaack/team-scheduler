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
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
#import MySQLdb
import os
from dotenv import load_dotenv
from pprint import pprint

##### Set up #####

load_dotenv() # add variables to the environment

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

class User(Base) :
  __table__ = Base.metadata.tables['user']

  email = __table__.columns['email']
  username = __table__.columns['username']
  password = __table__.columns['password']

  def __repr__(self) :
    return f'User(name: {self.username}; email: {self.email})'
  
class AvailabilityBlock(Base) :
  __table__ = Base.metadata.tables['availability_block']

  id = __table__.columns['availability_block_id']
  start_day = __table__.columns['start_day']
  end_day = __table__.columns['end_day']
  start_time = __table__.columns['start_time']
  end_time = __table__.columns['end_time']

  user_email = __table__.columns['user_email']
  # TODO look into many to one relationships
   
  def __repr__(self) :
    return f'AvailabilityBlock(availability_block_id: {self.availability_block_id})'
  
class Group(Base) :
  __table__ = Base.metadata.tables['group']

  id = __table__.columns['group_id']
  name = __table__.columns['group_name']
  description = __table__.columns['group_description']
   
  def __repr__(self) :
    return f'Group(group_id: {self.group_id}; group_name: {self.group_name})'
  
class Team(Base) :
  __table__ = Base.metadata.tables['team']

  id = __table__.columns['team_id']
  name = __table__.columns['team_name']
  description = __table__.columns['team_description']

  group_id = __table__.columns['group_id']
  #TODO many to one relationship
   
  def __repr__(self) :
    return f'Team(team_id: {self.team_id}; team_name: {self.team_name})'
  
class Event(Base) :
  __table__ = Base.metadata.tables['event']

  id = __table__.columns['event_id']
  name = __table__.columns['event_name']
  end_date = __table__.columns['end_date']
  reg_start_day = __table__.columns['reg_start_day']
  reg_end_day = __table__.columns['reg_end_day']
  start_time = __table__.columns['start_time']
  end_time = __table__.columns['end_time']
  description = __table__.columns['event_description']
  edit_permission = __table__.columns['edit_permission']

  group_id = __table__.columns['group_id']
  team_id = __table__.columns['team_id']
  # todo many to one relationships
   
  def __repr__(self) :
    return f'Group(event_id: {self.event_id}; event_name: {self.event_name})'
  

####### TESTING ########
@app.route('/')
def user_table () :
  query_str = ''
  for row in db.session.scalars(db.select(User.password)):
    #query_str += str(row) + '\n'
    query_str += str(row) + ' '
  return query_str

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('FLASK_PORT'))
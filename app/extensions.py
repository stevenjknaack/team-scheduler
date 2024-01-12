# Flask-SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
  """ Base for Models """
  """def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)"""
  pass

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# Sync Base's metadata with the current db
engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Base.metadata.reflect(engine)

from flask_sqlalchemy import SQLAlchemy
db: SQLAlchemy = SQLAlchemy(model_class=Base)

# Flask-Mail
from flask_mail import Mail
mail = Mail()
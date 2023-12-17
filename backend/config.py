import os
from dotenv import load_dotenv

load_dotenv() # load environment

class Config:
  # secret key
  SECRET_KEY = os.getenv('SECRET_KEY')

  # configure the flask_sqlalchemy
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # configure Flask-Mail API
  MAIL_SERVER = os.getenv('MAIL_SERVER')
  MAIL_PORT = os.getenv('MAIL_PORT')
  MAIL_USE_TLS = True
  MAIL_USE_SSL = False
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
  MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

  # TODO move to development config later
  # FLASK_DEBUG = True

  # TODO create testing config
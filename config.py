import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DATABASE_URL')
            or 'sqlite:///' + os.path.join(basedir, 'studystack.sqlite')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


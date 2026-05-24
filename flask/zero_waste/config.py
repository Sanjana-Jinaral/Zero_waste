import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-12345')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/zerowaste.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key')
    
    # Absolute path for SQLite to prevent 'unable to open database file' errors
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
        db_file = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        if not os.path.isabs(db_file):
             SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_file).replace('\\', '/')

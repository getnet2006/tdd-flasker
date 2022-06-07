from pathlib import Path

basedir = Path(__file__).resolve().parent

class Config(object):
    """
    Common configurations
    """
    DATABASE = 'flasker.db'
    USERNAME = 'admin'
    PASSWORD = 'admin'
    SECRET_KEY = 'development key' 
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
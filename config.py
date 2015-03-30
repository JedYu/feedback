import os
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
SECRET_KEY = 'airimos'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'issues.db')
EXPORT_PATH = os.path.join(_basedir, 'app/static/export/')
del os
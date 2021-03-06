import os


# path to project
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_precious'


DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (DATABASE_PATH,)
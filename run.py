from app import app as application
from db import db
from flask.cli import with_appcontext

db.init_app(application)

@application.before_first_request
@with_appcontext
def create_table():
    db.create_all()
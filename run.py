from app import app as application
from db import db

db.init_app(application)

@application.before_first_request
def create_table():
    db.create_all()
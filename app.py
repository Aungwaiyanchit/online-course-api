import os
from flask import Flask
from flask_restful import Api
from flask_uuid import FlaskUUID
from db import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import CreateUser


load_dotenv()


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True

app.secret_key=os.getenv("SERECT_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config["SQLALCHEMY_MODIFICATION"] = False

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(CreateUser, "/users/create")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000)
import datetime
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
from resources.course import CreateCourse, CourseLists, GetCourseByInstructorId, UpdateCourse, DeleteCourse, GetCourseByTopic, EnrollCourse
from resources.catagory import CreateCatagory, DeleteCatagory

load_dotenv()


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True

app.secret_key=os.getenv("SERECT_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"]= datetime.timedelta(minutes=60)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config["SQLALCHEMY_MODIFICATION"] = False

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_table():
    db.create_all()

#endpoints for users
api.add_resource(CreateUser, "/users/create")
# api.add_resource()

#endpoints for courses
api.add_resource(CourseLists, "/courses/all")
api.add_resource(CreateCourse, "/courses/create")
api.add_resource(UpdateCourse, "/courses/update")
api.add_resource(DeleteCourse, "/courses/delete")
api.add_resource(GetCourseByInstructorId, "/courses/getByInstructorId")
api.add_resource(GetCourseByTopic, "/courses/getByTopic")
api.add_resource(EnrollCourse, "/courses/enroll")

#endpoints for catagories
# api.add_resource('fa', "/catagories/all")
api.add_resource(CreateCatagory, "/catagories/create")
api.add_resource(DeleteCatagory, "/catagories/delete")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000)
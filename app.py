import datetime
import os
from flask import Flask
from flask_restful import Api
from flask_uuid import FlaskUUID
from db import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager


from resources.user import CreateUser, StudentEnrollCourse, UserLogin
from resources.course import CreateCourse, CourseLists, GetCourseByInstructorId, UpdateCourse, DeleteCourse, GetCourseByTopic, EnrollCourse, SearchCourse
from resources.catagory import CreateCatagory, DeleteCatagory, CatagoryList

load_dotenv()


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True

app.secret_key=os.getenv("SERECT_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"]= datetime.timedelta(hours=1)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DB_URI")
app.config["SQLALCHEMY_MODIFICATION"] = False

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

api = Api(app)

jwt = JWTManager(app)


#endpoints for users
api.add_resource(CreateUser, "/users/create")
api.add_resource(UserLogin, "/auth/login")
# api.add_resource()

#endpoints for courses
api.add_resource(CourseLists, "/courses/all")
api.add_resource(CreateCourse, "/courses/create")
api.add_resource(UpdateCourse, "/courses/update")
api.add_resource(DeleteCourse, "/courses/delete")
api.add_resource(GetCourseByInstructorId, "/courses/getByInstructorId")
api.add_resource(GetCourseByTopic, "/courses/getByTopic")
api.add_resource(EnrollCourse, "/courses/enroll")
api.add_resource(SearchCourse, "/courses/search")
api.add_resource(StudentEnrollCourse, "/courses/enroll/all")


#endpoints for catagories
api.add_resource(CatagoryList, "/catagories/all")
api.add_resource(CreateCatagory, "/catagories/create")
api.add_resource(DeleteCatagory, "/catagories/delete")

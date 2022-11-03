import datetime
import os
from flask import Flask, render_template
from flask_restful import Api
from flask_uuid import FlaskUUID
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS





from resources.user import CreateUser, DeleteUser, StudentEnrollCourse, UserLogin, UserLists, TokenRefresh
from resources.course import CreateCourse, CourseLists, GetCourseByInstructorId, UpdateCourse, DeleteCourse, GetCourseByTopic, EnrollCourse, SearchCourse
from resources.catagory import CreateCatagory, DeleteCatagory, CatagoryList

load_dotenv()





app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.debug = True

try:
    prodURI = os.getenv('DATABASE_URL')
    prodURI = prodURI.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = prodURI

except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'


app.config["JWT_ACCESS_TOKEN_EXPIRES"]= datetime.timedelta(hours=1)
app.config["JWT_SECRET_KEY"]=os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_MODIFICATION"] = False

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

api = Api(app)
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims(identity):
    print('iden', identity)
    if identity == "87dda76f-83ac-470c-8f75-86ba16d8809a":
        return { "is_admin": True }
    return { "is_admin": False }

@app.route("/")
def index():
    return render_template('index.html')

#endpoints for users
api.add_resource(CreateUser, "/users/create")
api.add_resource(DeleteUser, "/users/delete")
api.add_resource(UserLists, "/users/all")

api.add_resource(UserLogin, "/auth/login")
api.add_resource(TokenRefresh, "/auth/refresh")


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




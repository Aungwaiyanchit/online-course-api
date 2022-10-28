from models.course import CourseModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db


class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="username cannot be empty."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="username cannot be empty."
    )
    parser.add_argument(
        'user_type',
        type=str,
        required=True,
        help="user type cannot be empty"
    )
   
    # @jwt_required()
    def post(self):
        data = CreateUser.parser.parse_args()

        old_user = UserModel.find_user_by_username(data["username"])
        if old_user:
            return {
                "status": 409,
                "message": "usename already exists."
            }

        new_user = UserModel(data["username"], data["password"], data["user_type"])

        try:
            new_user.save_to_db()
        except:
            return {
                "status": 500,
                "message": "an error occured while creating user."
            }
        return {
            "status": 201,
            "message": "user created successfully."
        }



class StudentEnrollCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "student_id",
        type=str,
        required=True,
        help="student id cannot be blank"
    )

    def post(self):
        data = StudentEnrollCourse.parser.parse_args()

        student = UserModel.find_user_by_user_id(data["student_id"])
        if student is None:
            return { "message": "student not found."}, 404
        return {
            "enrolled coures": [c.json() for c in student.courses]
        }
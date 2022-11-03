from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt


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
            } , 500
        return {
            "status": 201,
            "message": "user created successfully."
        } , 201

class DeleteUser(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'user_id',
        type=str,
        required=True,
        help="user id cannot be blank."
    )

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return { "message": "Only admin can delete the user." }, 401

        data = DeleteUser.parser.parse_args()
        user = UserModel.find_user_by_user_id(data["user_id"])
        if user is None:
            return { "status": 404, "message": "user not found" } , 404
        try:
            UserModel.delete_user_by_id(data["user_id"])
        except:
            return { "status": 500, "message": "an error occuured while deleting user." }, 500
        return { "message": "user successfully deleted." }


class UserLogin(Resource):
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

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_user_by_username(data["username"])
       
        if user is None:
            return { "status": 401, "message": "Invalid Credential."}, 401
        match_password = check_password_hash(user.password, data["password"])
        if not match_password:
            return { "status": 401, "message": "Invalid Credential."}, 401
        #payload = {"userid": user.id, "username": user.username, "user_type": user.user_type}
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
            "status": 200,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return { 'access_token': new_token }, 200

class UserLists(Resource):
    def get(self):
        users = UserModel.get_all()
        return { "users": [user.json() for user in users]}
   


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
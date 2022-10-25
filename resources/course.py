from models.course import CourseModel
from flask_restful import Resource, reqparse

class CreateCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=str,
        help="course cannot be empty."
    )
    parser.add_argument(
        "descriptions",
        type=str,
        help="descriptions cannot be empty."
    )
    parser.add_argument(
        "instructor_id",
        type=str,
        help="instructor_id cannot be empty."
    )

    def post(self):
        data = CreateCourse.parser.parse_args()

        new_course = CourseModel(data["name"], data["descriptions"], data["instructor_id"])

        try:
            new_course.save_to_db()
        except:
            return { "message": "an error occred while creating course." }, 500
        
        return {
            "message": "course created successfully."
        }
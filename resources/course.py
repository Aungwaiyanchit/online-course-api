from email import parser
from models.course import CourseModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from models.topic import TopicModel
from flask_jwt import jwt_required


class CourseLists(Resource):

    jwt_required()
    def get(self):
        courses = CourseModel.get_courses_lists()
        for c in courses:
            print(c.json())
        return { "courses": [course.json() for course in courses] }


class CreateCourse(Resource):          
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=str,
        required=True,
        help="course cannot be empty."
    )
    parser.add_argument(
        "descriptions",
        type=str,
        required=True,
        help="descriptions cannot be empty."
    )
    parser.add_argument(
        "catagory_id",
        type=str,
        required=True,
        help="catagory_id cannot be empty."
    )
    parser.add_argument(
        "instructor_id",
        type=str,
        required=True,
        help="instructor_id cannot be empty."
    )
    parser.add_argument(
        "topics",
        type=str,
        action='append',
        help="tags must be lists"
    )

    jwt_required()
    def post(self):
        data = CreateCourse.parser.parse_args()
        user = UserModel.find_user_by_user_id(data["instructor_id"])
        if user.user_type != "instructor":
            return { "message": "student cannot create course." }
        new_course = CourseModel(data["name"], data["descriptions"], data["catagory_id"], data["instructor_id"], )
        topics = []
        for topic in data["topics"]:
            old_topic = TopicModel.find_tags_by_name(topic)
            if old_topic is not None:
                topics.append(old_topic)
            else:
               new_topic = TopicModel(topic)
               topics.append(new_topic)
        try:
            for topic in topics:
                new_course.topics.append(topic)
            new_course.save_to_db()
        except BaseException as err:
            return { "message": f"an error occred while creating course. {err}" }, 500
        
        return { "status": 201, "message": "course created successfully." }


class UpdateCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "course_id",
        type=str,
        required=True,
        help="course_id cannot be empty"
    )
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
    parser.add_argument(
        "topics",
        type=str,
        action='append',
        help="tags must be lists"
    )

    jwt_required()
    def post(self):
        data = CreateCourse.parser.parse_args()
        user = UserModel.find_user_by_user_id(data["instructor_id"])
        if user.user_type != "instructor":
            return { "message": "student cannot create course." }
        new_course = CourseModel(data["name"], data["descriptions"], data["instructor_id"])
        topics = []
        for topic in data["topics"]:
            old_topic = TopicModel.find_tags_by_name(topic)
            if old_topic is not None:
                topics.append(old_topic)
            else:
               new_topic = TopicModel(topic)
               topics.append(new_topic)
        try:
            for topic in topics:
                new_course.topics.append(topic)
            new_course.save_to_db()
        except BaseException as err:
            return { "message": f"an error occred while creating course. {err}" }, 500
        
        return { "message": "course updated successfully." }


class DeleteCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "course_id",
        type=str,
        required=True,
        help="course_id cannot be empty"
    ) 

    jwt_required()
    def post(self):
        return
class GetCourseByInstructorId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "instructor_id",
        type=str,
        required=True,
        help="Instructor id cannot be empty."
    )

    jwt_required()
    def post(self):
        data = GetCourseByInstructorId.parser.parse_args()

        courses = CourseModel.get_course_by_instructor_id(data["instructor_id"])

        return { "courses": [course.json() for course in courses] }

class GetCourseByTopic(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "topic",
        type=str
    )

    jwt_required()
    def post(self):
        data = GetCourseByTopic.parser.parse_args()

        courses = CourseModel.get_course_by_topics(data["topic"])
        return { "courses": [courses.json() for course in courses] }
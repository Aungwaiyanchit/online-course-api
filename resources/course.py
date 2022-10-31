from models.course import CourseModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from models.topic import TopicModel
from flask_jwt_extended import jwt_required
from db import db



class CourseLists(Resource):

    @jwt_required()
    def get(self):
        courses = CourseModel.get_courses_lists()
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
    parser.add_argument(
        "img_url",
        type=str,
        location='files'
    )
    

    @jwt_required()
    def post(self):
        data = CreateCourse.parser.parse_args()
        user = UserModel.find_user_by_user_id(data["instructor_id"])
        if user is None:
            return { "message": "invalid user id." }
        if user.user_type != "instructor":
            return { "message": "student cannot create course." }
        old_course = CourseModel.get_course_by_name(data["name"])
        if old_course is not None:
            return { "message": "course name is already exists." }
        new_course = CourseModel(data["name"], data["descriptions"], data["catagory_id"], data["instructor_id"])
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
            return { "message": "an error occred while creating course." }, 500
        
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
        "instructor_id",
        type=str,
        required=True,
        help="instructor cannot be empty"
    )
    parser.add_argument(
        "catagory_id",
        type=str,
        required=True,
        help="instructor cannot be empty"
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
        "topics",
        type=str,
        action='append',
        help="tags must be lists"
    )

    @jwt_required()
    def post(self):
        data = UpdateCourse.parser.parse_args()
        user = UserModel.find_user_by_user_id(data["instructor_id"])
        if user.user_type != "instructor":
            return { "message": "student cannot update course." }
        
        topics = []
        for topic in data["topics"]:
            old_topic = TopicModel.find_tags_by_name(topic)
            if old_topic is not None:
                topics.append(old_topic)
            else:
               new_topic = TopicModel(topic)
               topics.append(new_topic)
        
        try:
            CourseModel.update_course(data["course_id"], data["name"], data["descriptions"], data["catagory_id"], topics)
            course = CourseModel.get_course_by_id(data["course_id"])
            course.topics = topics
            db.session.commit()
        except BaseException as err:
            print(err)
            return { "message": "an error occured while updating." }, 500
        
        return { "message": "course updated successfully." }


class DeleteCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "course_id",
        type=str,
        required=True,
        help="course_id cannot be empty"
    ) 

    @jwt_required()
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

    @jwt_required()
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

    @jwt_required()
    def post(self):
        data = GetCourseByTopic.parser.parse_args()

        courses = CourseModel.get_course_by_topics(data["topic"])
        return { "courses": [course.json() for course in courses] }


class EnrollCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "student_id",
        type=str,
        required=True,
        help="student id cannot be blank."
    )
    parser.add_argument(
        "course_id",
        type=str,
        required=True,
        help="student id cannot be blank."
    )

    @jwt_required()
    def post(self):
        data =EnrollCourse.parser.parse_args()

        student = UserModel.find_user_by_user_id(data["student_id"])
        if student.user_type != "student":
            return { "message": "only student can enroll course." }
        
        already_enroll = UserModel.get_enroll_course(data["course_id"])
        if already_enroll is not None:
            return { "message": "course already enrolled." }
        
        course = CourseModel.get_course_by_id(data["course_id"])
        student.courses.append(course)
        db.session.commit()
        return { "message": "course enroll successfully." }


class SearchCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=str,
        required=True,
        help="name cannot be blank."
    )

    def post(self):
        data = SearchCourse.parser.parse_args()

        courses = CourseModel.get_course_by_name_lists(data["name"])
        return { "courses": [course.json() for course in courses]}
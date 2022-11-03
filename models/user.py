from importlib.resources import Resource
from db import db
import uuid
from flask_bcrypt import generate_password_hash


student_courses = db.Table('student_courses',
    db.Column('user_id', db.String(80), db.ForeignKey('users.id')),
    db.Column('course_id', db.String(80), db.ForeignKey('courses.id')),
)

class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    user_type = db.Column(db.String())
    courses = db.relationship('CourseModel', secondary=student_courses, lazy="dynamic", backref='users')

    def __init__(self, username, password, user_type):
        self.username = username
        self.password = generate_password_hash(password, 10).decode('utf-8')
        self.user_type = user_type   

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod
    def find_user_by_user_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def get_enroll_course(cls, id):
        return cls.query.filter(cls.courses.any(id=id)).first()
    
    @classmethod
    def delete_user_by_id(cls, id):
        delete_user = cls.query.filter(cls.id==id).delete()
        db.session.commit()
        return delete_user

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def json(self):
        return { "id": self.id, "name": self.username, "type": self.user_type }


    
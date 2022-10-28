import uuid
from db import db
from models.catagory import CatagoryModel


course_topics = db.Table('course_topics',
    db.Column('course_id', db.String(80), db.ForeignKey('courses.id')),
    db.Column('topic_id', db.String(80), db.ForeignKey('topics.id')),   
)

class CourseModel(db.Model):

    __tablename__="courses"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    descriptions = db.Column(db.Text())
    catagory_id = db.Column(db.String(80), db.ForeignKey('catagories.id'))
    instructor_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    topics = db.relationship('TopicModel', secondary=course_topics, lazy="dynamic", backref='courses')

    catagory = db.relationship('CatagoryModel',)
    instructor = db.relationship('UserModel',)

    def __init__(self, name, descriptions,catagory_id, instructor_id):
        self.name = name
        self.descriptions = descriptions
        self.catagory_id = catagory_id
        self.instructor_id = instructor_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self): 
        return { 
            "id": self.id, 
            "name": self.name, 
            "descriptions": self.descriptions,
            "catagory": self.catagory.json(),
            "instructor": self.instructor.json(),
            "topics": [topic.name for topic in self.topics]
            }

    @classmethod
    def get_courses_lists(cls):
        return cls.query.all()

    @classmethod
    def update_course(cls, course_id, name, descriptions, catagory_id):
        update_course = cls.query.filter(CourseModel.id==course_id).update({
            "name":name,
            "descriptions":descriptions,
            "catagory_id" : catagory_id,
            })
        db.session.commit()
        return update_course

    @classmethod
    def get_course_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
        
    @classmethod
    def get_course_by_instructor_id(cls, instructor_id):
        return cls.query.filter_by(instructor_id=instructor_id)
    
    @classmethod
    def get_course_by_topics(cls, topics):
        return cls.query.filter(CourseModel.topics.any(name=topics)).all()
    
    
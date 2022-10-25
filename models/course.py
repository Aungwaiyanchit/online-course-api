import uuid
from db import db

class CourseModel(db.Model):

    __tablename__="courses"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    descriptions = db.Column(db.Text())
    #catagory_id = db.Column(db.String(80), db.ForeignKey('catagories.id'))
    instructor_id = db.Column(db.String(80), db.ForeignKey('users.id'))

    def __init__(self, name, descriptions, instructor_id):
        self.name = name
        self.descriptions = descriptions
        self.instructor_id = instructor_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_course_by_instructor_id(self):
        return 
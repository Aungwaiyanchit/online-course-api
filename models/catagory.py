import uuid
from app import db


class CatagoryModel(db.Model):

    __tablename__="catagories"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))

    courses = db.relationship("CourseModel", lazy="dynamic", backref="catagories")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_catagory_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def delete_catagory_by_name(cls, name):
        delete_catagory = cls.query.filter(CatagoryModel.name==name).delete()
        db.session.commit()
        return delete_catagory

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self):
        return { 'id': self.id, "name": self.name, "courses": [ course.id for course in self.courses ] }
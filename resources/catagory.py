from models.catagory import CatagoryModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class CreateCatagory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="name cannot be empty."
    )

    jwt_required()
    def post(self):
        data = CreateCatagory.parser.parse_args()
        old_catagory = CatagoryModel.find_catagory_by_name(data["name"])
        if old_catagory is not None:
            return { "status": 409, "message": "catagory name already exisits." }
        new_catagory = CatagoryModel(data["name"])
        try:
            new_catagory.save_to_db()
        except:
            return { "status": 500, "message": "an error occured while creating catagory." }, 500
        return { "status": 201, "message": "catagory successfully created." }, 201


class DeleteCatagory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="name cannot be empty."
    )

    jwt_required()
    def post(self):
        data = DeleteCatagory.parser.parse_args()
        old_catagory = CatagoryModel.find_catagory_by_name(data["name"])
        if old_catagory is None:
            return { "status": 404, "message": "catagory not found." }, 404
        try:
            CatagoryModel.delete_catagory_by_name(data["name"])
        except:
            return { "status": 200, "message": "an error occured while deleting catagory." }
        return { "status": 200, "message": "catagory successfully deleted." }

class CatagoryList(Resource):

    def get(self):
        catagories = CatagoryModel.get_all()
        return {
            "categories": [catagory.json() for catagory in catagories]
        }
        
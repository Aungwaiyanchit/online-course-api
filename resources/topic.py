# from models.tag import TagModel
# from flask_restful import Resource, reqparse

# class CreateTag(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument(
#         "name",
#         type=str,
#         required=True,
#         help="name cannot be empty."
#     )
    
#     def post(self):
#         data = CreateTag.parser.parse_args()

#         new_tag = TagModel(data["name"])

#         try:
#             new_tag.save_to_db()
#         except:
#             return {
#                  "status": 500,
#                  "message": "an error occured while creating tag." 
#                  }, 500
#         return { 
#             "status": 201,
#             "message": "tag create successfully." 
#             }, 201

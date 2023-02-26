from flask import Blueprint, request
from flask_restful import Api, Resource
from .. import db
from ..model.comment import Comment

comment_blueprint = Blueprint("comment", __name__)
comment_api = Api(comment_blueprint)

class CommentsAPI(Resource):
  def get(self):
    id = request.args.get("id")
    comment = db.session.query(Comment).get(id)
    if comment:
      return comment.to_dict()
    return {"message": "player not found"}, 404

  def post(self):
    name = request.args.get("name")
    body = request.args.get("body")
    
    new_comment = Comment(name=name, body=body)
    print(new_comment.to_dict())
    if new_comment:
      db.session.add(new_comment)
      db.session.commit()
      return
    return {"message": "error creating comment"}, 404

  def delete(self):
    id = request.args.get("id")
    comment = db.session.query(Comment).get(id)
    try:
      db.session.add(comment)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return "error while creating comment: " + str(e)
    return {"message": "error creating comment"}, 404
  
class ListComments(Resource):
  def get(self):
    comment = db.session.query(Comment).all()
    return [comment.to_dict() for comment in comment]
  
comment_api.add_resource(ListComments, "/list-comments")
comment_api.add_resource(CommentsAPI, "/comments")
from flask import Blueprint, request
from flask_restful import Api, Resource
from .. import db, User

quiz_blueprint = Blueprint("quiz", __name__)
quiz_api = Api(quiz_blueprint)

class Correct(Resource):
  def get(self):
    id = request.args.get("id")
    user = db.session.query(User).get(id)

    if user:
      return user.to_dict()
    return "error getting user", 400

  def put(self):
    id = request.args.get("id")
    user = db.session.query(User).get(id)

    if user:
      user.incrementCorrect()
      db.session.commit()
      return user.correct
    return "error incrementing correct num", 400

class Incorrect(Resource):
  def put(self):
    id = request.args.get("id")
    user = db.session.query(User).get(id)

    if user:
      user.incrementIncorrect()
      db.session.commit()
      return user.incorrect
    return "error incrementing incorrect num", 400
  
class ListQuizzes(Resource):
  def get(self):
    users = db.session.query(User).all()
    return [user.to_dict() for user in users]
  
quiz_api.add_resource(ListQuizzes, "/list-quizzes")
quiz_api.add_resource(Correct, "/correct")
quiz_api.add_resource(Incorrect, "/incorrect")
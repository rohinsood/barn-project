from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import RegisterForm, db
from ..model.nba_player import Players

player_blueprint = Blueprint("players", __name__)
player_api = Api(player_blueprint)

class PlayersAPI(Resource):
  def get(self):
    name = request.args.get("name")
    player = db.session.query(Players).filter_by(_name_id=name.lower()).first()
    if player:
      return player.to_dict()
    return {"message": "driver not found"}, 404

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("id", required=True, type=int)
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("comment", required=True, type=str)
    args = parser.parse_args()

    try:
      driver = db.session.query(Players).get(args["id"])
      if driver:
        driver.comments = {
          "name": args["name"],
          "comment": args["comment"]
        }
        db.session.commit()
      else:
          return {"message": "driver not found"}, 404
    except Exception as e:
      db.session.rollback()
      return {"message": f"server error: {e}"}, 500
  
  def delete(self):
    id = request.args.get("id")
    driver = db.session.query(Players).get(id)

    if driver:
      driver.deleteComment()
      db.session.commit()
      return driver.to_dict()
    return {"message": "driver not found"}, 404

class Likes(Resource):
  def put(self):
    id = request.args.get("id")
    driver = db.session.query(Players).get(id)

    if driver:
      driver.like()
      db.session.commit()
      return driver.likes
    return {"message": "driver not found"}, 404

class Dislikes(Resource):
  def put(self):
    id = request.args.get("id")
    driver = db.session.query(Players).get(id)

    if driver:
      driver.dislike()
      db.session.commit()
      return driver.dislikes
    return {"message": "driver not found"}, 404

class ListPlayers(Resource):
  def get(self):
    players = db.session.query(Players).all()
    return [player.to_dict() for player in players]

player_api.add_resource(PlayersAPI, "/players")
player_api.add_resource(Likes, "/like")
player_api.add_resource(Dislikes, "/dislike")
player_api.add_resource(ListPlayers, "/players-list")
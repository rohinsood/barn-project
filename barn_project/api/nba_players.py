from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.nba_player import NBAPlayers

player_blueprint = Blueprint("players", __name__)
player_api = Api(player_blueprint)

class NBAPlayersAPI(Resource):
  def get(self):
    name = request.args.get("name")
    player = db.session.query(NBAPlayers).filter_by(_name_id=name.lower()).first()
    if player:
      return player.to_dict()
    return {"message": "player not found"}, 404

class Likes(Resource):
  def put(self):
    id = request.args.get("id")
    player = db.session.query(NBAPlayers).get(id)

    if player:
      player.like()
      db.session.commit()
      return player.likes
    return {"message": "player not found"}, 404

class Dislikes(Resource):
  def put(self):
    id = request.args.get("id")
    player = db.session.query(NBAPlayers).get(id)

    if player:
      player.dislike()
      db.session.commit()
      return player.dislikes
    return {"message": "player not found"}, 404

class ListPlayers(Resource):
  def get(self):
    players = db.session.query(NBAPlayers).all()
    return [player.to_dict() for player in players]

player_api.add_resource(NBAPlayersAPI, "/nba-players")
player_api.add_resource(Likes, "/like")
player_api.add_resource(Dislikes, "/dislike")
player_api.add_resource(ListPlayers, "/nba-list")
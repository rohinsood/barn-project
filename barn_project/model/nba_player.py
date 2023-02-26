import requests
from sqlalchemy import Column, Integer, PickleType, String
from .. import db

class Players(db.Model):
  id = Column(Integer, primary_key=True)
  _name = Column(String(255))
  _name_id = Column(String(255))
  _team = Column(String(255))
  _position = Column(Integer)

  _likes = Column(Integer)
  _dislikes = Column(Integer)
  _comments = Column(PickleType)

  def __init__(self, player_name, team_name, position):
    self._name = player_name
    self._team = team_name
    self._position = position

    self._name_id = player_name.lower()

    self._likes = 0
    self._dislikes = 0
    self._comments = []

  @property
  def name(self):
    return self._name

  @property
  def team(self):
    return self._team

  @property
  def standings(self):
    return self._position

  @property
  def nationality(self):
    return self._nationality

  @property
  def likes(self) -> int:
    return self._likes

  @property
  def dislikes(self) -> int:
    return self._dislikes

  @property
  def comments(self) -> list:
    return self._comments

  @comments.setter
  def comments(self, comment: dict):
    self._comments = self.comments + [comment.copy()]

  def addComment(self, comment):
    self._comments.append(comment)


  def deleteComment(self):
    self._comments = self.comments[:-1].copy()

  def like(self):
    self._likes += 1

  def dislike(self):
    self._dislikes += 1

  def to_dict(self):
    return {"name": self._name, "team": self._team, "position": self._position,  "likes": self._likes, "dislikes": self._dislikes, "comments": str(self._comments)}

def init_players():

  if not len(db.session.query(Players).all()) == 0:
    return

  all_players = []

  for page_num in range(1, 39):
    headers = {
        "X-RapidAPI-Key": "9275b62a1fmsh3b832340dafb492p1abc77jsn58ef554feee6",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }

    querystring = {"page":str(page_num),"per_page":"100"}

    r = requests.get(
      url="https://free-nba.p.rapidapi.com/players", headers=headers, params=querystring)

    if r.status_code != 200:
      print("API Request failed:", r.status_code)
      exit

    all_players.extend(r.json()['data'])

  player_objects = []

  for player in all_players:
    full_name = player["first_name"] + " " + player["last_name"]

    player_objects.append(
        Players(player_name=full_name, team_name=player["team"]["full_name"],
               position=player["position"])
    )

  player_objects[0].addComment({
      "name": "Dontavious",
      "message": "You're trash!!"
  })
  [player_objects[0].dislike() for i in range(20)]

  player_objects[1].addComment({
      "name": "Dontavious",
      "message": "Mid tbh"
  })
  [player_objects[1].like() for i in range(20)]

  player_objects[2].addComment({
      "name": "Dontavious",
      "message": "3.0/3.0: Great job! You deserve some seed points."
  })
  [player_objects[2].like() for i in range(3)]

  for player in player_objects:
    try:
      db.session.add(player)
      db.session.commit()
    except Exception as e:
      print("error while creating players: " + str(e))
      db.session.rollback()

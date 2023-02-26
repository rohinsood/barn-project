from sqlalchemy import Column, Integer, String
from .. import db

class Comment(db.Model):
  id = Column(Integer, primary_key=True)
  _name = Column(String(255))
  _body = Column(String(255))
  
  def __init__(self, name, body):
    self._name = name
    self._body = body

  @property
  def name(self):
    return self._name
  
  @property
  def body(self):
    return self._body

  @body.setter
  def body(self, comment: str):
    self._body = comment

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "body": self.body,
    }

def init_comments():
  if not len(db.session.query(Comment).all()) == 0:
    return
  
  comments = [
    [
      "Jamal", "LeBron my goat fr 😘"
    ],
    [
      "Dontavious", "LeBron lowk dogwater tbh"
    ],
  ]

  comment_objects = [Comment(comment[0], comment[1]) for comment in comments]
  for comment in comment_objects:
    try:
      db.session.add(comment)
      db.session.commit()
    except Exception as e:
      print("error while creating comment: " + str(e))
      db.session.rollback()
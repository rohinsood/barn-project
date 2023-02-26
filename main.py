from barn_project import app, db
from barn_project.api import nba_players, comments
from barn_project.model import nba_player, comment
from flask_cors import CORS

app.register_blueprint(nba_players.player_blueprint)
app.register_blueprint(comments.comment_blueprint)

@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        nba_player.init_players()
        comment.init_comments()

if __name__ == "__main__":
  cors = CORS(app)
  app.run(debug=True, host="0.0.0.0", port="8086")
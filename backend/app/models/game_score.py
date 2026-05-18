from app.extensions import db


class GameScore(db.Model):
    __tablename__ = "game_scores"

    game_score_id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.game_id"),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.team_id"),
        nullable=False
    )

    score_value = db.Column(db.Float, nullable=False)
    rank_position = db.Column(db.Integer, nullable=True)
    isWinner = db.Boolean(db.Boolean, nullable=False, default=False)

    game = db.relationship(
        "Game",
        back_populates="game_scores"
    )

    team = db.relationship(
        "Team",
        back_populates="game_scores"
    )

    score_components = db.relationship(
        "ScoreComponent",
        back_populates="game_score",
        cascade="all, delete-orphan"
    )
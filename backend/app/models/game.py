from app.extensions import db


class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)

    event_sport_id = db.Column(
        db.Integer,
        db.ForeignKey("event_sports.event_sport_id"),
        nullable=False
    )

    game_date = db.Column(db.DateTime)
    round = db.Column(db.String(100))
    status = db.Column(db.String(50))

    event_sport = db.relationship(
        "EventSport",
        back_populates="games"
    )

    game_scores = db.relationship(
        "GameScore",
        back_populates="game",
        cascade="all, delete-orphan"
    )   
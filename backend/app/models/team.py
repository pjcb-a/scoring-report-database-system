from app.extensions import db


class Team(db.Model):
    __tablename__ = "teams"

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150), nullable=False, unique=True)
    team_color = db.Column(db.String(50), nullable=False)

    game_scores = db.relationship(
        "GameScore",
        back_populates="team",
        cascade="all, delete-orphan"
    )
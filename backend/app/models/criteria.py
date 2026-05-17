from app.extensions import db


class Criteria(db.Model):
    __tablename__ = "criteria"

    criteria_id = db.Column(db.Integer, primary_key=True)

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sports.sport_id"),
        nullable=False
    )

    criteria_name = db.Column(db.String(150), nullable=False)
    percentage_weight = db.Column(db.Float, nullable=False)

    sport = db.relationship(
        "Sport",
        back_populates="criteria"
    )

    score_components = db.relationship(
        "ScoreComponent",
        back_populates="criteria",
        cascade="all, delete-orphan"
    )
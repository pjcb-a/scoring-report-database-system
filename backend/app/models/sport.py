from app.extensions import db


class Sport(db.Model):
    __tablename__ = "sports"

    sport_id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String(100), nullable=False, unique=True)

    scoring_id = db.Column(
        db.Integer,
        db.ForeignKey("scoring_types.scoring_id"),
        nullable=False
    )

    scoring_type = db.relationship(
        "ScoringType",
        back_populates="sports"
    )

    event_sports = db.relationship(
        "EventSport",
        back_populates="sport",
        cascade="all, delete-orphan"
    )

    criteria = db.relationship(
        "Criteria",
        back_populates="sport",
        cascade="all, delete-orphan"
    )
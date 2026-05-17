from app.extensions import db


class EventSport(db.Model):
    __tablename__ = "event_sports"

    event_sport_id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.event_id"),
        nullable=False
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sports.sport_id"),
        nullable=False
    )

    venue = db.Column(db.String(150))
    schedule = db.Column(db.DateTime)
    status = db.Column(db.String(50))

    event = db.relationship(
        "Event",
        back_populates="event_sports"
    )

    sport = db.relationship(
        "Sport",
        back_populates="event_sports"
    )

    games = db.relationship(
        "Game",
        back_populates="event_sport",
        cascade="all, delete-orphan"
    )
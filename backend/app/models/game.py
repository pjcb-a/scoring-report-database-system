from app.extensions import db


class Game(db.Model):

    __tablename__ = "games"

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    game_id = db.Column(
        db.Integer,
        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEY
    --------------------------------------------------------------------------
    """

    event_sport_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "event_sports.event_sport_id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    start_date = db.Column(
        db.DateTime,
        nullable=False
    )

    end_date = db.Column(
        db.DateTime
    )

    venue_name = db.Column(
        db.String(150)
    )

    game_status = db.Column(
        db.String(50),
        nullable=False
    )

    round = db.Column(
        db.String(100)
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event_sport = db.relationship(
        "EventSport",
        back_populates="games"
    )

    game_scores = db.relationship(
        "GameScore",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "game_id":
            self.game_id,

            "event_sport_id":
            self.event_sport_id,

            "event_id":
            self.event_sport.event_id,

            "sport_id":
            self.event_sport.sport_id,

            "event":
            self.event_sport.event.event_name,

            "sport":
            self.event_sport.sport.sport_name,

            "sport_name":
            self.event_sport.sport.sport_name,

            "scoring_type_id":
            self.event_sport.sport.scoring_type_id,

            "scoring_type":
            self.event_sport.sport.scoring_type.type
            if self.event_sport.sport.scoring_type
            else None,

            "start_date":
            self.start_date.isoformat()
            if self.start_date
            else None,

            "end_date":
            self.end_date.isoformat()
            if self.end_date
            else None,

            "venue_name":
            self.venue_name,

            "game_status":
            self.game_status,

            "round":
            self.round
        }

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
    FOREIGN KEYS
    --------------------------------------------------------------------------
    """

    event_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "events.event_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

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

    game_name = db.Column(

        db.String(150),

        nullable=False
    )

    start_date = db.Column(

        db.DateTime,

        nullable=True
    )

    end_date = db.Column(

        db.DateTime,

        nullable=True
    )

    venue_name = db.Column(

        db.String(150),

        nullable=True
    )

    game_status = db.Column(

        db.String(50),

        nullable=False,

        default="Scheduled"
    )

    round = db.Column(

        db.String(100),

        nullable=True
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event = db.relationship(

        "Event",

        back_populates="games",
        lazy="selectin"
    )

    event_sport = db.relationship(

        "EventSport",

        back_populates="games",
        lazy="selectin"
    )

    game_scores = db.relationship(

        "GameScore",

        back_populates="game",

        cascade="all, delete-orphan",
        lazy="selectin"
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

            "event_id":
                self.event_id,

            "event_sport_id":
                self.event_sport_id,

            "game_name":
                self.game_name,

            "event":
                self.event.event_name
                if self.event
                else None,

            "sport":
                self.event_sport.sport.sport_name
                if self.event_sport
                and self.event_sport.sport
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
from app.extensions import db


class EventSport(db.Model):

    __tablename__ = "event_sports"

    __table_args__ = (

        db.UniqueConstraint(

            "event_id",

            "sport_id",

            name="uq_event_sport"
        ),
    )

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    event_sport_id = db.Column(

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

    sport_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "sports.sport_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    venue = db.Column(

        db.String(150),

        nullable=True
    )

    schedule = db.Column(

        db.DateTime,

        nullable=True
    )

    status = db.Column(

        db.String(50),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

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

    criteria = db.relationship(

        "Criteria",

        back_populates="event_sport",

        cascade="all, delete-orphan"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "event_sport_id":
                self.event_sport_id,

            "event_id":
                self.event_id,

            "sport_id":
                self.sport_id,

            "event":
                self.event.event_name
                if self.event
                else None,

            "sport":
                self.sport.sport_name
                if self.sport
                else None,

            "scoring_type":
                self.sport.scoring_type.type
                if (
                    self.sport
                    and self.sport.scoring_type
                )
                else None,

            "venue":
                self.venue,

            "schedule":
                self.schedule.isoformat()
                if self.schedule
                else None,

            "status":
                self.status
        }
from app.extensions import db


class Criteria(db.Model):

    __tablename__ = "criteria"

    __table_args__ = (

        db.UniqueConstraint(

            "event_sport_id",

            "criteria_name",

            name="uq_event_sport_criteria"
        ),
    )

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    criteria_id = db.Column(

        db.Integer,

        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEYS
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

    criteria_name = db.Column(

        db.String(150),

        nullable=False
    )

    percentage = db.Column(

        db.Float,

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event_sport = db.relationship(

        "EventSport",

        back_populates="criteria"
    )

    score_components = db.relationship(

        "ScoreComponent",

        back_populates="criteria",

        cascade="all, delete-orphan"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "criteria_id":
                self.criteria_id,

            "event_sport_id":
                self.event_sport_id,

            "criteria_name":
                self.criteria_name,

            "percentage":
                self.percentage,

            "sport":
                self.event_sport.sport.sport_name
                if self.event_sport
                and self.event_sport.sport
                else None,

            "event":
                self.event_sport.event.event_name
                if self.event_sport
                and self.event_sport.event
                else None
        }
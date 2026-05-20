from app.extensions import db


class Team(db.Model):

    __tablename__ = "teams"

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    team_id = db.Column(
        db.Integer,
        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    EVENT OWNERSHIP
    --------------------------------------------------------------------------
    """

    event_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "events.event_id"
        ),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    team_name = db.Column(

        db.String(150),

        nullable=False
    )

    team_color = db.Column(

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

        back_populates="teams"
    )

    game_scores = db.relationship(

        "GameScore",

        back_populates="team",

        cascade="all, delete-orphan"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "team_id":
            self.team_id,

            "event_id":
            self.event_id,

            "team_name":
            self.team_name,

            "team_color":
            self.team_color,

            "event":
            self.event.event_name
            if self.event else None
        }

    """
    --------------------------------------------------------------------------
    STRING REPRESENTATION
    --------------------------------------------------------------------------
    """

    def __repr__(self):

        return (
            f"<Team "
            f"{self.team_name}>"
        )
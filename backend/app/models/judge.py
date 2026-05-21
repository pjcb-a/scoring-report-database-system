from app.extensions import db


class Judge(db.Model):

    __tablename__ = "judges"

    __table_args__ = (

        db.UniqueConstraint(

            "event_id",

            "judge_name",

            name="uq_event_judge_name"
        ),
    )

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    judge_id = db.Column(

        db.Integer,

        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEY
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

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    judge_name = db.Column(

        db.String(150),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event = db.relationship(

        "Event",

        back_populates="judges"
    )

    score_components = db.relationship(

        "ScoreComponent",

        back_populates="judge",

        cascade="all, delete-orphan"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "judge_id":
                self.judge_id,

            "event_id":
                self.event_id,

            "judge_name":
                self.judge_name,

            "event":
                self.event.event_name
                if self.event
                else None
        }
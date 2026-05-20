from app.extensions import db


class Judge(db.Model):

    __tablename__ = "judges"

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
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    judge_name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

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

            "judge_name":
            self.judge_name
        }

    """
    --------------------------------------------------------------------------
    STRING REPRESENTATION
    --------------------------------------------------------------------------
    """

    def __repr__(self):

        return (
            f"<Judge "
            f"{self.judge_name}>"
        )

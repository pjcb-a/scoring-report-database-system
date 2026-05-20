from app.extensions import db


class Criteria(db.Model):
    __tablename__ = "criteria"
    __table_args__ = (
        db.UniqueConstraint(
            "sport_id",
            "criteria_name",
            name="uq_criteria_sport_name"
        ),
    )

    criteria_id = db.Column(db.Integer, primary_key=True)

    """
    --------------------------------------------------------------------------
    FOREIGN KEYS
    --------------------------------------------------------------------------
    """

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey("sports.sport_id", ondelete="CASCADE"),
        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    criteria_name = db.Column(db.String(150), nullable=False)
    percentage_weight = db.Column(db.Float, nullable=False)

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """


    sport = db.relationship(
        "Sport",
        back_populates="criteria"
    )

    score_components = db.relationship(
        "ScoreComponent",
        back_populates="criteria",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "criteria_id": self.criteria_id,
            "sport_id": self.sport_id,
            "sport": self.sport.sport_name if self.sport else None,
            "criteria_name": self.criteria_name,
            "percentage_weight": self.percentage_weight
        }

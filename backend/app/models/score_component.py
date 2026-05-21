from app.extensions import db


class ScoreComponent(db.Model):

    __tablename__ = "score_components"

    __table_args__ = (

        db.UniqueConstraint(

            "game_score_id",

            "criteria_id",

            "judge_id",

            name="uq_score_component"
        ),
    )

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    score_component_id = db.Column(

        db.Integer,

        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEYS
    --------------------------------------------------------------------------
    """

    game_score_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "game_scores.game_score_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    criteria_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "criteria.criteria_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    judge_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "judges.judge_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    score_value = db.Column(

        db.Float,

        nullable=False
    )

    weighted_score = db.Column(

        db.Float,

        nullable=True
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    game_score = db.relationship(

        "GameScore",

        back_populates="score_components",
        lazy="selectin"
    )

    criteria = db.relationship(

        "Criteria",

        back_populates="score_components",
        lazy="selectin"
    )

    judge = db.relationship(

        "Judge",

        back_populates="score_components",
        lazy="selectin"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "score_component_id":
                self.score_component_id,

            "game_score_id":
                self.game_score_id,

            "criteria_id":
                self.criteria_id,

            "judge_id":
                self.judge_id,

            "team":
                self.game_score.team.team_name
                if (
                    self.game_score
                    and self.game_score.team
                )
                else None,

            "criteria":
                self.criteria.criteria_name
                if self.criteria
                else None,

            "judge":
                self.judge.judge_name
                if self.judge
                else None,

            "score_value":
                self.score_value,

            "weighted_score":
                self.weighted_score
        }
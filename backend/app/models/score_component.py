from app.extensions import db


class ScoreComponent(db.Model):
    __tablename__ = "score_components"

    score_component_id = db.Column(db.Integer, primary_key=True)

    game_score_id = db.Column(
        db.Integer,
        db.ForeignKey("game_scores.game_score_id"),
        nullable=False
    )

    criteria_id = db.Column(
        db.Integer,
        db.ForeignKey("criteria.criteria_id"),
        nullable=False
    )

    judge_id = db.Column(
        db.Integer,
        db.ForeignKey("judges.judge_id"),
        nullable=False
    )

    score_value = db.Column(db.Float, nullable=False)

    game_score = db.relationship(
        "GameScore",
        back_populates="score_components"
    )

    criteria = db.relationship(
        "Criteria",
        back_populates="score_components"
    )

    judge = db.relationship(
        "Judge",
        back_populates="score_components"
    )
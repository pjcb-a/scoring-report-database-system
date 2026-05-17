from app.extensions import db


class Judge(db.Model):
    __tablename__ = "judges"

    judge_id = db.Column(db.Integer, primary_key=True)
    raw_score = db.Column(db.Integer, nullable=False)

    score_components = db.relationship(
        "ScoreComponent",
        back_populates="judge",
        cascade="all, delete-orphan"
    )
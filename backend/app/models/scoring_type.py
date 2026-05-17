from app.extensions import db


class ScoringType(db.Model):
    __tablename__ = "scoring_types"

    scoring_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    sports = db.relationship(
        "Sport",
        back_populates="scoring_type"
    )
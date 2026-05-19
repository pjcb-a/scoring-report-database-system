from app.extensions import db


class Team(db.Model):
    __tablename__ = "teams"

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150), nullable=False, unique=True)
    team_color = db.Column(db.String(50), nullable=False)

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

            'team_id':
            self.team_id,

            'team_name':
            self.team_name,

            'team_color':
            self.team_color
        }

    """
    --------------------------------------------------------------------------
    STRING REPRESENTATION
    --------------------------------------------------------------------------
    """

    def __repr__(self):

        return (
            f'<Team '
            f'{self.team_name}>'
        )
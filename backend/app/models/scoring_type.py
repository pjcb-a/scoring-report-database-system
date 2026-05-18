from app.extensions import db


class ScoringType(db.Model):

    __tablename__ = 'scoring_types'

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    scoring_type_id = db.Column(
        db.Integer,
        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    type = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    sports = db.relationship(
        'Sport',
        back_populates='scoring_type'
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {
            'scoring_type_id':
            self.scoring_type_id,

            'type':
            self.type,

            'description':
            self.description
        }
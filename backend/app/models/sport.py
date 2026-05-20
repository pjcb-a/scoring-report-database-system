from app.extensions import db


class Sport(db.Model):

    __tablename__ = 'sports'

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    sport_id = db.Column(
        db.Integer,
        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEYS
    --------------------------------------------------------------------------
    """

    scoring_type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'scoring_types.scoring_type_id',
            ondelete='RESTRICT'
        ),
        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    sport_name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    scoring_type = db.relationship(
        'ScoringType',
        back_populates='sports'
    )

    event_sports = db.relationship(
        'EventSport',
        back_populates='sport',
        cascade='all, delete-orphan'
    )

    criteria = db.relationship(
        'Criteria',
        back_populates='sport',
        cascade='all, delete-orphan'
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            'sport_id':
            self.sport_id,

            'sport_name':
            self.sport_name,

            'scoring_type_id':
            self.scoring_type_id,

            'scoring_type':
            self.scoring_type.type
            if self.scoring_type
            else None
        }

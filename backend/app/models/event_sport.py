from app.extensions import db


class EventSport(db.Model):

    __tablename__ = 'event_sports'

    event_sport_id = db.Column(
        db.Integer,
        primary_key=True
    )

    """
    --------------------------------------------------------------------------
    FOREIGN KEYS
    --------------------------------------------------------------------------
    """

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.event_id'),
        nullable=False
    )

    sport_id = db.Column(
        db.Integer,
        db.ForeignKey('sports.sport_id'),
        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    venue = db.Column(
        db.String(150),
        nullable=True
    )

    schedule = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event = db.relationship(
        'Event',
        back_populates='event_sports'
    )

    sport = db.relationship(
        'Sport',
        back_populates='event_sports'
    )

    games = db.relationship(
        'Game',
        back_populates='event_sport',
        cascade='all, delete-orphan'
    )

    def to_dict(self):

        return {

            'event_sport_id':
            self.event_sport_id,

            'event':
            self.event.event_name,

            'sport':
            self.sport.sport_name,

            'venue':
            self.venue,

            'schedule':
            str(self.schedule),

            'status':
            self.status
        }
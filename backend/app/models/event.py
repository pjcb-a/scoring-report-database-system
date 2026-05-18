from app.extensions import db


class Event(db.Model):

    __tablename__ = 'events'

    event_id = db.Column(
        db.Integer,
        primary_key=True
    )

    event_name = db.Column(
        db.String(150),
        nullable=False
    )

    start_day = db.Column(
        db.Date,
        nullable=False
    )

    end_day = db.Column(
        db.Date,
        nullable=False
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

    event_sports = db.relationship(
        'EventSport',
        back_populates='event',
        cascade='all, delete-orphan'
    )

    def to_dict(self):

        return {
            'event_id':
            self.event_id,

            'event_name':
            self.event_name,

            'start_day':
            str(self.start_day),

            'end_day':
            str(self.end_day),

            'status':
            self.status
        }
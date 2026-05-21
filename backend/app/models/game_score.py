from app.extensions import db


class GameScore(db.Model):

    __tablename__ = "game_scores"

    __table_args__ = (

        db.UniqueConstraint(

            "game_id",

            "team_id",

            name="uq_game_team"
        ),
    )

    """
    --------------------------------------------------------------------------
    PRIMARY KEY
    --------------------------------------------------------------------------
    """

    game_score_id = db.Column(

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

        db.ForeignKey(

            "events.event_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    game_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "games.game_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    team_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "teams.team_id",

            ondelete="CASCADE"
        ),

        nullable=False
    )

    """
    --------------------------------------------------------------------------
    ATTRIBUTES
    --------------------------------------------------------------------------
    """

    total_score = db.Column(

        db.Float,

        nullable=False,

        default=0
    )

    rank_position = db.Column(

        db.Integer,

        nullable=True
    )

    is_winner = db.Column(

        db.Boolean,

        nullable=False,

        default=False
    )

    """
    --------------------------------------------------------------------------
    RELATIONSHIPS
    --------------------------------------------------------------------------
    """

    event = db.relationship(

        "Event",

        back_populates="game_scores",
        lazy="selectin"
    )

    game = db.relationship(

        "Game",

        back_populates="game_scores",
        lazy="selectin"
    )

    team = db.relationship(

        "Team",

        back_populates="game_scores",
        lazy="selectin"
    )

    score_components = db.relationship(

        "ScoreComponent",

        back_populates="game_score",

        cascade="all, delete-orphan",
        lazy="selectin"
    )

    """
    --------------------------------------------------------------------------
    SERIALIZER
    --------------------------------------------------------------------------
    """

    def to_dict(self):

        return {

            "game_score_id":
                self.game_score_id,

            "event_id":
                self.event_id,

            "game_id":
                self.game_id,

            "team_id":
                self.team_id,

            "team":
                self.team.team_name
                if self.team
                else None,

            "team_color":
                self.team.team_color
                if self.team
                else None,

            "event":
                self.event.event_name
                if self.event
                else None,

            "sport":
                self.game.event_sport.sport.sport_name
                if (
                    self.game
                    and self.game.event_sport
                    and self.game.event_sport.sport
                )
                else None,

            "total_score":
                self.total_score,

            "rank_position":
                self.rank_position,

            "is_winner":
                self.is_winner
        }
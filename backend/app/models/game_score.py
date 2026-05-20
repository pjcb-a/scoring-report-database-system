from app.extensions import db


class GameScore(db.Model):
    __tablename__ = "game_scores"
    __table_args__ = (
        db.UniqueConstraint(
            "game_id",
            "team_id",
            name="uq_game_scores_game_team"
        ),
    )

    game_score_id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.game_id", ondelete="CASCADE"),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.team_id", ondelete="CASCADE"),
        nullable=False
    )

    score_value = db.Column(db.Float, nullable=False)
    rank_position = db.Column(db.Integer, nullable=True)
    isWinner = db.Column(db.Boolean, nullable=False, default=False)

    game = db.relationship(
        "Game",
        back_populates="game_scores"
    )

    team = db.relationship(
        "Team",
        back_populates="game_scores"
    )

    score_components = db.relationship(
        "ScoreComponent",
        back_populates="game_score",
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "game_score_id": self.game_score_id,
            "game_id": self.game_id,
            "team_id": self.team_id,
            "team": self.team.team_name if self.team else None,
            "team_color": self.team.team_color if self.team else None,
            "score_value": self.score_value,
            "rank_position": self.rank_position,
            "isWinner": self.isWinner,
            "event": self.game.event_sport.event.event_name
            if self.game and self.game.event_sport
            else None,
            "sport": self.game.event_sport.sport.sport_name
            if self.game and self.game.event_sport
            else None,
            "scoring_type": self.game.event_sport.sport.scoring_type.type
            if (
                self.game
                and self.game.event_sport
                and self.game.event_sport.sport
                and self.game.event_sport.sport.scoring_type
            )
            else None,
            "round": self.game.round if self.game else None
        }

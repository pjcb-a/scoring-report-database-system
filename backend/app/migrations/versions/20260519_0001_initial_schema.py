"""Initial local PostgreSQL schema.

Revision ID: 20260519_0001
Revises:
Create Date: 2026-05-19
"""

from alembic import op
import sqlalchemy as sa


revision = "20260519_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "events",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("event_name", sa.String(length=150), nullable=False),
        sa.Column("start_day", sa.Date(), nullable=False),
        sa.Column("end_day", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("event_id")
    )

    op.create_table(
        "judges",
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("judge_name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("judge_id"),
        sa.UniqueConstraint("judge_name")
    )

    op.create_table(
        "scoring_types",
        sa.Column("scoring_type_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("scoring_type_id"),
        sa.UniqueConstraint("type")
    )

    op.create_table(
        "teams",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("team_name", sa.String(length=150), nullable=False),
        sa.Column("team_color", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("team_id"),
        sa.UniqueConstraint("team_name")
    )

    scoring_type_table = sa.table(
        "scoring_types",
        sa.column("type", sa.String),
        sa.column("description", sa.Text)
    )

    op.bulk_insert(
        scoring_type_table,
        [
            {
                "type": "Win/Lose",
                "description": "Head-to-head competition scoring."
            },
            {
                "type": "Incremental",
                "description": "Points accumulated progressively."
            },
            {
                "type": "Threshold Incremental",
                "description": "Placement-based point assignment."
            },
            {
                "type": "Ranked Timed",
                "description": "Fastest or shortest completion wins."
            },
            {
                "type": "Component Score",
                "description": "Judge-based criteria scoring."
            }
        ]
    )

    op.create_table(
        "sports",
        sa.Column("sport_id", sa.Integer(), nullable=False),
        sa.Column("scoring_type_id", sa.Integer(), nullable=False),
        sa.Column("sport_name", sa.String(length=150), nullable=False),
        sa.ForeignKeyConstraint(
            ["scoring_type_id"],
            ["scoring_types.scoring_type_id"],
            ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("sport_id"),
        sa.UniqueConstraint("sport_name")
    )

    op.create_table(
        "criteria",
        sa.Column("criteria_id", sa.Integer(), nullable=False),
        sa.Column("sport_id", sa.Integer(), nullable=False),
        sa.Column("criteria_name", sa.String(length=150), nullable=False),
        sa.Column("percentage_weight", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.sport_id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("criteria_id"),
        sa.UniqueConstraint(
            "sport_id",
            "criteria_name",
            name="uq_criteria_sport_name"
        )
    )

    op.create_table(
        "event_sports",
        sa.Column("event_sport_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("sport_id", sa.Integer(), nullable=False),
        sa.Column("venue", sa.String(length=150), nullable=True),
        sa.Column("schedule", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.event_id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.sport_id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("event_sport_id"),
        sa.UniqueConstraint(
            "event_id",
            "sport_id",
            name="uq_event_sports_event_sport"
        )
    )

    op.create_table(
        "games",
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("event_sport_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("venue_name", sa.String(length=150), nullable=True),
        sa.Column("game_status", sa.String(length=50), nullable=False),
        sa.Column("round", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_sport_id"],
            ["event_sports.event_sport_id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("game_id")
    )

    op.create_table(
        "game_scores",
        sa.Column("game_score_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("score_value", sa.Float(), nullable=False),
        sa.Column("rank_position", sa.Integer(), nullable=True),
        sa.Column("isWinner", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.game_id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.team_id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("game_score_id"),
        sa.UniqueConstraint(
            "game_id",
            "team_id",
            name="uq_game_scores_game_team"
        )
    )

    op.create_table(
        "score_components",
        sa.Column("score_component_id", sa.Integer(), nullable=False),
        sa.Column("game_score_id", sa.Integer(), nullable=False),
        sa.Column("criteria_id", sa.Integer(), nullable=False),
        sa.Column("judge_id", sa.Integer(), nullable=False),
        sa.Column("score_value", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["criteria_id"],
            ["criteria.criteria_id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["game_score_id"],
            ["game_scores.game_score_id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["judge_id"],
            ["judges.judge_id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("score_component_id"),
        sa.UniqueConstraint(
            "game_score_id",
            "criteria_id",
            "judge_id",
            name="uq_score_components_score_criteria_judge"
        )
    )


def downgrade():
    op.drop_table("score_components")
    op.drop_table("game_scores")
    op.drop_table("games")
    op.drop_table("event_sports")
    op.drop_table("criteria")
    op.drop_table("sports")
    op.drop_table("teams")
    op.drop_table("scoring_types")
    op.drop_table("judges")
    op.drop_table("events")

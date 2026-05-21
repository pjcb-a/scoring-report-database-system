"""
|--------------------------------------------------------------------------
| MODEL IMPORTS
|--------------------------------------------------------------------------
|
| Centralized model registry.
|
| Import order matters because of SQLAlchemy relationship resolution.
|
"""


from .event import Event

from .team import Team

from .sport import Sport

from .scoring_type import ScoringType

from .event_sport import EventSport

from .criteria import Criteria

from .judge import Judge

from .game import Game

from .game_score import GameScore

from .score_component import ScoreComponent


"""
|--------------------------------------------------------------------------
| EXPORTED MODELS
|--------------------------------------------------------------------------
"""

__all__ = [

    "Event",

    "Team",

    "Sport",

    "ScoringType",

    "EventSport",

    "Criteria",

    "Judge",

    "Game",

    "GameScore",

    "ScoreComponent"
]
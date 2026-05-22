from flask import Blueprint, request

from app.extensions import db

from app.models.game import Game
from app.models.game_score import GameScore
from app.models.event import Event
from app.models.event_sport import EventSport
from app.models.team import Team
from app.models.criteria import Criteria
from app.models.judge import Judge
from app.models.score_component import ScoreComponent


ALLOWED_GAME_STATUSES = {
    'Win',
    'Forfeit',
    'Suspensions'
}

THRESHOLD_INCREMENTAL = 'Threshold Incremental'
COMPONENT_SCORE = 'Component Score'

from app.routes.utils import (
    parse_datetime,
    clean_string
)

from app.utils.responses import (

    success_response,

    error_response
)


game_bp = Blueprint(

    'game_bp',

    __name__
)


"""
|--------------------------------------------------------------------------
| GET GAMES BY EVENT
|--------------------------------------------------------------------------
|
| Returns all games under a specific event.
|
"""


@game_bp.route(

    '/events/<int:event_id>/games',

    methods=['GET']
)
def get_event_games(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        scheduled_only = request.args.get(
            'scheduled_only',
            'false'
        ).lower() in (
            '1',
            'true',
            'yes'
        )

        query = Game.query.filter_by(
            event_id=event_id
        )

        if scheduled_only:
            query = query.filter_by(
                is_finalized=False
            )

        games = query.all()

        data = [

            game.to_dict()

            for game in games
        ]

        return success_response(

            data=data,

            message='Games fetched successfully.'
        )

    except Exception as e:

        return error_response(

            message='Failed to fetch games.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| CREATE GAME
|--------------------------------------------------------------------------
|
| Creates a game under an event.
|
"""


@game_bp.route(

    '/events/<int:event_id>/games',

    methods=['POST']
)
def create_game(event_id):

    try:

        event = Event.query.get(event_id)

        if not event:

            return error_response(

                message='Event not found.',

                status_code=404
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        event_sport_id = payload.get(
            'event_sport_id'
        )

        game_name = clean_string(
            payload.get('game_name')
        )

        set_count_raw = payload.get('set_count')

        team_ids_raw = payload.get(
            'team_ids',
            []
        )

        round_name = clean_string(
            payload.get('round')
        )

        venue_name = clean_string(
            payload.get('venue_name')
            or payload.get('venue')
        )

        start_raw = (
            payload.get('start_date')
            or payload.get('start_time')
        )

        end_raw = (
            payload.get('end_date')
            or payload.get('end_time')
        )

        """
        ----------------------------------------------------------------------
        VALIDATION
        ----------------------------------------------------------------------
        """

        validation_errors = {}

        if not event_sport_id:

            validation_errors[
                'event_sport_id'
            ] = [

                'Event sport is required.'
            ]

        if not isinstance(team_ids_raw, list):

            validation_errors[
                'team_ids'
            ] = [

                'Teams must be provided as a list.'
            ]

        team_ids = []

        if isinstance(team_ids_raw, list):

            for team_id in team_ids_raw:

                try:

                    team_ids.append(int(team_id))

                except (TypeError, ValueError):

                    validation_errors[
                        'team_ids'
                    ] = [

                        'Each team id must be a valid integer.'
                    ]

                    break

            team_ids = list(dict.fromkeys(team_ids))

        if not team_ids:

            validation_errors[
                'team_ids'
            ] = [

                'Select at least one team for this game.'
            ]

        if validation_errors:

            return error_response(

                message='Validation failed.',

                errors=validation_errors,

                status_code=400
            )

        """
        ----------------------------------------------------------------------
        VALIDATE EVENT SPORT
        ----------------------------------------------------------------------
        """

        event_sport = EventSport.query.filter_by(

            event_sport_id=event_sport_id,

            event_id=event_id

        ).first()

        if not event_sport:

            return error_response(

                message='Invalid event sport.',

                status_code=400
            )

        validated_teams = []

        for team_id in team_ids:

            team = Team.query.filter_by(

                team_id=team_id,

                event_id=event_id

            ).first()

            if not team:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'team_ids': [
                            f'Team {team_id} is not part of this event.'
                        ]
                    },

                    status_code=400
                )

            validated_teams.append(team)

        scoring_type_name = (
            event_sport.sport.scoring_type.type
            if event_sport.sport
            and event_sport.sport.scoring_type
            else None
        )

        set_count = None

        if scoring_type_name == THRESHOLD_INCREMENTAL:

            try:

                set_count = int(set_count_raw)

            except (TypeError, ValueError):

                return error_response(

                    message='Validation failed.',

                    errors={
                        'set_count': [
                            'Number of sets is required for Threshold Incremental sports.'
                        ]
                    },

                    status_code=400
                )

            if set_count < 1:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'set_count': [
                            'Number of sets must be at least 1.'
                        ]
                    },

                    status_code=400
                )

        start_date, start_error = parse_datetime(
            start_raw,
            'Start time'
        )

        if start_error:

            return error_response(

                message='Validation failed.',

                errors={
                    'start_time': [start_error]
                },

                status_code=400
            )

        end_date, end_error = parse_datetime(
            end_raw,
            'End time'
        )

        if end_error:

            return error_response(

                message='Validation failed.',

                errors={
                    'end_time': [end_error]
                },

                status_code=400
            )

        if not game_name:

            sport_label = (
                event_sport.sport.sport_name
                if event_sport.sport
                else 'Game'
            )

            game_name = (
                f"{sport_label} - {round_name}"
                if round_name
                else sport_label
            )

        """
        ----------------------------------------------------------------------
        CREATE GAME
        ----------------------------------------------------------------------
        """

        game = Game(

            event_id=event_id,

            event_sport_id=event_sport_id,

            game_name=game_name,

            start_date=start_date,

            end_date=end_date,

            venue_name=venue_name,

            game_status='Pending',

            round=round_name,

            set_count=set_count,

            is_finalized=False
        )

        db.session.add(game)

        db.session.flush()

        for team in validated_teams:

            db.session.add(

                GameScore(

                    event_id=event_id,

                    game_id=game.game_id,

                    team_id=team.team_id,

                    total_score=0,

                    is_winner=False
                )
            )

        db.session.commit()

        return success_response(

            data=game.to_dict(),

            message='Game created successfully.',

            status_code=201
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to create game.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| UPDATE GAME
|--------------------------------------------------------------------------
|
| Updates a game.
|
"""


@game_bp.route(

    '/games/<int:game_id>',

    methods=['PUT']
)
def update_game(game_id):

    try:

        game = Game.query.get(game_id)

        if not game:

            return error_response(

                message='Game not found.',

                status_code=404
            )

        if game.is_finalized:

            return error_response(

                message='Finalized matches cannot be edited. View them under Reports.',

                status_code=400
            )

        payload = request.get_json()

        if not payload:

            return error_response(

                message='Request body is required.',

                status_code=400
            )

        scoring_type_name = (
            game.event_sport.sport.scoring_type.type
            if game.event_sport
            and game.event_sport.sport
            and game.event_sport.sport.scoring_type
            else None
        )

        if 'game_name' in payload:

            game.game_name = clean_string(
                payload.get('game_name')
            ) or game.game_name

        if 'event_sport_id' in payload:

            event_sport_id = payload.get(
                'event_sport_id'
            )

            event_sport = EventSport.query.filter_by(

                event_sport_id=event_sport_id,

                event_id=game.event_id

            ).first()

            if not event_sport:

                return error_response(

                    message='Invalid event sport.',

                    status_code=400
                )

            game.event_sport_id = event_sport_id

        start_raw = (
            payload.get('start_date')
            if 'start_date' in payload
            else payload.get('start_time')
            if 'start_time' in payload
            else None
        )

        if start_raw is not None:

            start_date, start_error = parse_datetime(
                start_raw,
                'Start time'
            )

            if start_error:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'start_time': [start_error]
                    },

                    status_code=400
                )

            game.start_date = start_date

        end_raw = (
            payload.get('end_date')
            if 'end_date' in payload
            else payload.get('end_time')
            if 'end_time' in payload
            else None
        )

        if end_raw is not None:

            end_date, end_error = parse_datetime(
                end_raw,
                'End time'
            )

            if end_error:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'end_time': [end_error]
                    },

                    status_code=400
                )

            game.end_date = end_date

        if 'venue_name' in payload or 'venue' in payload:

            game.venue_name = clean_string(
                payload.get('venue_name')
                or payload.get('venue')
            )

        if 'round' in payload:

            game.round = clean_string(
                payload.get('round')
            )

        if 'set_count' in payload:

            if scoring_type_name != THRESHOLD_INCREMENTAL:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'set_count': [
                            'Set count applies only to Threshold Incremental sports.'
                        ]
                    },

                    status_code=400
                )

            try:

                set_count = int(payload.get('set_count'))

            except (TypeError, ValueError):

                return error_response(

                    message='Validation failed.',

                    errors={
                        'set_count': [
                            'Number of sets must be a valid integer.'
                        ]
                    },

                    status_code=400
                )

            if set_count < 1:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'set_count': [
                            'Number of sets must be at least 1.'
                        ]
                    },

                    status_code=400
                )

            game.set_count = set_count

        if 'team_ids' in payload:

            team_ids_raw = payload.get('team_ids', [])

            if not isinstance(team_ids_raw, list):

                return error_response(

                    message='Validation failed.',

                    errors={
                        'team_ids': ['Teams must be provided as a list.']
                    },

                    status_code=400
                )

            team_ids = []

            for team_id in team_ids_raw:

                try:

                    team_ids.append(int(team_id))

                except (TypeError, ValueError):

                    return error_response(

                        message='Validation failed.',

                        errors={
                            'team_ids': [
                                'Each team id must be a valid integer.'
                            ]
                        },

                        status_code=400
                    )

            team_ids = list(dict.fromkeys(team_ids))

            if not team_ids:

                return error_response(

                    message='Validation failed.',

                    errors={
                        'team_ids': [
                            'Select at least one team for this game.'
                        ]
                    },

                    status_code=400
                )

            for team_id in team_ids:

                team = Team.query.filter_by(

                    team_id=team_id,

                    event_id=game.event_id

                ).first()

                if not team:

                    return error_response(

                        message='Validation failed.',

                        errors={
                            'team_ids': [
                                f'Team {team_id} is not part of this event.'
                            ]
                        },

                        status_code=400
                    )

            existing_by_team = {
                score.team_id: score
                for score in game.game_scores
            }

            new_team_ids = set(team_ids)

            for team_id, game_score in existing_by_team.items():

                if team_id not in new_team_ids:

                    db.session.delete(game_score)

            for team_id in new_team_ids:

                if team_id not in existing_by_team:

                    db.session.add(
                        GameScore(
                            event_id=game.event_id,
                            game_id=game.game_id,
                            team_id=team_id,
                            total_score=0,
                            is_winner=False
                        )
                    )

        db.session.commit()

        return success_response(

            data=game.to_dict(),

            message='Game updated successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to update game.',

            errors=[str(e)],

            status_code=500
        )


"""
|--------------------------------------------------------------------------
| DELETE GAME
|--------------------------------------------------------------------------
|
| Deletes a game.
|
"""


@game_bp.route(
    '/games/<int:game_id>/finalize',
    methods=['POST']
)
def finalize_game(game_id):
    try:
        game = Game.query.get(game_id)

        if not game:
            return error_response(
                message='Game not found.',
                status_code=404
            )

        if game.is_finalized:
            return error_response(
                message='This match is already finalized.',
                status_code=400
            )

        payload = request.get_json()

        if not payload:
            return error_response(
                message='Request body is required.',
                status_code=400
            )

        game_status = clean_string(
            payload.get('game_status')
        )

        if game_status not in ALLOWED_GAME_STATUSES:
            return error_response(
                message='Validation failed.',
                errors={
                    'game_status': [
                        'Game status must be Win, Forfeit, or Suspensions.'
                    ]
                },
                status_code=400
            )

        team_entries = payload.get('teams', [])

        if not isinstance(team_entries, list) or not team_entries:
            return error_response(
                message='Validation failed.',
                errors={
                    'teams': ['Provide score data for each team in this match.']
                },
                status_code=400
            )

        scoring_type_name = (
            game.event_sport.sport.scoring_type.type
            if game.event_sport
            and game.event_sport.sport
            and game.event_sport.sport.scoring_type
            else None
        )

        is_threshold = scoring_type_name == THRESHOLD_INCREMENTAL
        is_component = scoring_type_name == COMPONENT_SCORE

        game_scores_by_team = {
            score.team_id: score
            for score in game.game_scores
        }

        if set(game_scores_by_team.keys()) != {
            int(entry.get('team_id'))
            for entry in team_entries
            if entry.get('team_id') is not None
        }:
            return error_response(
                message='Validation failed.',
                errors={
                    'teams': ['Score data must be provided for every team in this match.']
                },
                status_code=400
            )

        if is_component:
            criteria_list = Criteria.query.filter_by(
                event_sport_id=game.event_sport_id
            ).all()

            if not criteria_list:
                return error_response(
                    message='Validation failed.',
                    errors={
                        'criteria': [
                            'This sport has no criteria. Add criteria on the Judging tab first.'
                        ]
                    },
                    status_code=400
                )

            criteria_by_id = {
                criterion.criteria_id: criterion
                for criterion in criteria_list
            }

            judges = Judge.query.filter_by(
                event_id=game.event_id
            ).all()

            if not judges:
                return error_response(
                    message='Validation failed.',
                    errors={
                        'judges': [
                            'Add at least one judge on the Judging tab before finalizing.'
                        ]
                    },
                    status_code=400
                )

            judges_by_id = {
                judge.judge_id: judge
                for judge in judges
            }

            expected_pairs = {
                (judge.judge_id, criterion.criteria_id)
                for judge in judges
                for criterion in criteria_list
            }

        winners = 0

        for entry in team_entries:
            team_id = entry.get('team_id')

            try:
                team_id = int(team_id)
            except (TypeError, ValueError):
                return error_response(
                    message='Validation failed.',
                    errors={'teams': ['Each team entry requires a valid team_id.']},
                    status_code=400
                )

            game_score = game_scores_by_team.get(team_id)

            if not game_score:
                return error_response(
                    message='Invalid team for this match.',
                    status_code=400
                )

            if is_component:
                judge_scores = entry.get('judge_scores', [])

                if not isinstance(judge_scores, list):
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'judge_scores': [
                                'Judge scores must be provided as a list.'
                            ]
                        },
                        status_code=400
                    )

                received_pairs = set()
                judge_weighted_totals = {}

                for judge_score in judge_scores:
                    criteria_id = judge_score.get('criteria_id')
                    judge_id = judge_score.get('judge_id')
                    score_value = judge_score.get('score_value')

                    try:
                        criteria_id = int(criteria_id)
                        judge_id = int(judge_id)
                        score_value = float(score_value)
                    except (TypeError, ValueError):
                        return error_response(
                            message='Validation failed.',
                            errors={
                                'judge_scores': [
                                    'Each judge score must include valid numbers.'
                                ]
                            },
                            status_code=400
                        )

                    pair = (judge_id, criteria_id)

                    if pair in received_pairs:
                        return error_response(
                            message='Validation failed.',
                            errors={
                                'judge_scores': [
                                    'Duplicate score for the same judge and criteria.'
                                ]
                            },
                            status_code=400
                        )

                    received_pairs.add(pair)

                    criterion = criteria_by_id.get(criteria_id)

                    if not criterion:
                        return error_response(
                            message='Invalid criteria for this sport.',
                            status_code=400
                        )

                    if judge_id not in judges_by_id:
                        return error_response(
                            message='Invalid judge for this event.',
                            status_code=400
                        )

                    weighted_score = (
                        score_value * (float(criterion.percentage) / 100)
                    )

                    judge_weighted_totals[judge_id] = (
                        judge_weighted_totals.get(judge_id, 0.0)
                        + weighted_score
                    )

                    db.session.add(
                        ScoreComponent(
                            game_score_id=game_score.game_score_id,
                            criteria_id=criteria_id,
                            judge_id=judge_id,
                            score_value=score_value,
                            weighted_score=weighted_score
                        )
                    )

                if received_pairs != expected_pairs:
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'judge_scores': [
                                'Provide a score from every judge for every criteria for each team.'
                            ]
                        },
                        status_code=400
                    )

                game_score.total_score = (
                    sum(judge_weighted_totals.values())
                    / len(judge_weighted_totals)
                )
                game_score.rank_position = None
                game_score.set_scores = None
                game_score.sets_won = None

            elif is_threshold:
                set_scores = entry.get('set_scores', [])

                if not isinstance(set_scores, list):
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'set_scores': ['Set scores must be provided as a list.']
                        },
                        status_code=400
                    )

                if len(set_scores) != game.set_count:
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'set_scores': [
                                f'Provide exactly {game.set_count} set scores for each team.'
                            ]
                        },
                        status_code=400
                    )

                try:
                    parsed_set_scores = [float(value) for value in set_scores]
                except (TypeError, ValueError):
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'set_scores': ['Each set score must be a valid number.']
                        },
                        status_code=400
                    )

                sets_won = entry.get('sets_won')

                try:
                    sets_won = int(sets_won)
                except (TypeError, ValueError):
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'sets_won': ['Sets won is required for each team.']
                        },
                        status_code=400
                    )

                game_score.set_scores = parsed_set_scores
                game_score.sets_won = sets_won
                game_score.total_score = float(sum(parsed_set_scores))
                game_score.rank_position = None

            else:
                total_score = entry.get('total_score')

                if total_score is None:
                    total_score = entry.get('score_value')

                if total_score is None:
                    return error_response(
                        message='Validation failed.',
                        errors={
                            'total_score': ['Score value is required for each team.']
                        },
                        status_code=400
                    )

                game_score.total_score = float(total_score)
                game_score.set_scores = None
                game_score.sets_won = None

                rank_position = entry.get('rank_position')

                if rank_position == '':
                    rank_position = None

                if rank_position is not None:
                    try:
                        game_score.rank_position = int(rank_position)
                    except (TypeError, ValueError):
                        return error_response(
                            message='Validation failed.',
                            errors={
                                'rank_position': ['Rank position must be a valid integer.']
                            },
                            status_code=400
                        )
                else:
                    game_score.rank_position = None

            is_winner = entry.get('is_winner')

            if is_winner is None:
                is_winner = entry.get('isWinner', False)

            game_score.is_winner = bool(is_winner)

            if game_score.is_winner:
                winners += 1

        game.game_status = game_status
        game.is_finalized = True

        db.session.commit()

        return success_response(
            data=game.to_dict(),
            message='Match finalized successfully.'
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Failed to finalize match.',
            errors=[str(e)],
            status_code=500
        )


@game_bp.route(

    '/games/<int:game_id>',

    methods=['DELETE']
)
def delete_game(game_id):

    try:

        game = Game.query.get(game_id)

        if not game:

            return error_response(

                message='Game not found.',

                status_code=404
            )

        if game.is_finalized:

            return error_response(

                message='Finalized matches cannot be deleted from Games. They are kept in Reports.',

                status_code=400
            )

        db.session.delete(game)

        db.session.commit()

        return success_response(

            message='Game deleted successfully.'
        )

    except Exception as e:

        db.session.rollback()

        return error_response(

            message='Failed to delete game.',

            errors=[str(e)],

            status_code=500
        )
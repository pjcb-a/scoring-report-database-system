from app.extensions import db

from app.models.scoring_type import (
    ScoringType
)


def seed_scoring_types():

    scoring_types = [

        {
            'type': 'Win/Lose',
            'description':
            'Head-to-head competition scoring.'
        },

        {
            'type': 'Incremental',
            'description':
            'Points accumulated progressively.'
        },

        {
            'type': 'Threshold Incremental',
            'description':
            'Placement-based point assignment.'
        },

        {
            'type': 'Ranked Timed',
            'description':
            'Fastest or shortest completion wins.'
        },

        {
            'type': 'Component Score',
            'description':
            'Judge-based criteria scoring.'
        }
    ]

    for item in scoring_types:

        existing = ScoringType.query.filter_by(
            type=item['type']
        ).first()

        if not existing:

            scoring_type = ScoringType(
                type=item['type'],
                description=item['description']
            )

            db.session.add(scoring_type)

    db.session.commit()

    print(
        'Scoring types seeded successfully.'
    )


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        seed_scoring_types()

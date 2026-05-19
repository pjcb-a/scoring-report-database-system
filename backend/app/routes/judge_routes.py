from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.judge import Judge


judge_bp = Blueprint(
    "judge_bp",
    __name__
)


"""
------------------------------------------------------------------------------
GET ALL JUDGES
------------------------------------------------------------------------------
"""

@judge_bp.route(
    "/api/judges",
    methods=["GET"]
)
def get_judges():

    judges = Judge.query.all()

    result = []

    for judge in judges:

        result.append({

            "judge_id":
            judge.judge_id,

            "judge_name":
            judge.judge_name
        })

    return jsonify(result)


"""
------------------------------------------------------------------------------
CREATE JUDGE
------------------------------------------------------------------------------
"""

@judge_bp.route(
    "/api/judges",
    methods=["POST"]
)
def create_judge():

    data = request.get_json()

    judge = Judge(

        judge_name=
        data["judge_name"]
    )

    db.session.add(judge)

    db.session.commit()

    return jsonify({

        "message":
        "Judge created successfully"
    }), 201


"""
------------------------------------------------------------------------------
UPDATE JUDGE
------------------------------------------------------------------------------
"""

@judge_bp.route(
    "/api/judges/<int:judge_id>",
    methods=["PUT"]
)
def update_judge(judge_id):

    judge = Judge.query.get_or_404(
        judge_id
    )

    data = request.get_json()

    judge.judge_name = data.get(
        "judge_name",
        judge.judge_name
    )

    db.session.commit()

    return jsonify({

        "message":
        "Judge updated successfully"
    })


"""
------------------------------------------------------------------------------
DELETE JUDGE
------------------------------------------------------------------------------
"""

@judge_bp.route(
    "/api/judges/<int:judge_id>",
    methods=["DELETE"]
)
def delete_judge(judge_id):

    judge = Judge.query.get_or_404(
        judge_id
    )

    db.session.delete(judge)

    db.session.commit()

    return jsonify({

        "message":
        "Judge deleted successfully"
    })
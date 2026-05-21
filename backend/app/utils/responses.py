from flask import jsonify


"""
|--------------------------------------------------------------------------
| SUCCESS RESPONSE
|--------------------------------------------------------------------------
|
| Standardized success response format.
|
| Example:
|
| {
|   "success": True,
|   "message": "...",
|   "data": ...
| }
|
"""


def success_response(

    data=None,

    message='Success.',

    status_code=200

):

    return jsonify({

        'success': True,

        'message': message,

        'data': data

    }), status_code


"""
|--------------------------------------------------------------------------
| ERROR RESPONSE
|--------------------------------------------------------------------------
|
| Standardized error response format.
|
| Example:
|
| {
|   "success": False,
|   "message": "...",
|   "errors": ...
| }
|
"""


def error_response(

    message='Something went wrong.',

    errors=None,

    status_code=400

):

    return jsonify({

        'success': False,

        'message': message,

        'errors': errors or []

    }), status_code
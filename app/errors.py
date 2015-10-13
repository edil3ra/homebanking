from flask import jsonify


class ValidationError(ValueError):
    pass


def not_modified():
    response = jsonify({'status': 304, 'error': 'not modified'})
    response.status_code = 304
    return response


def not_found(message):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': message})
    response.status_code = 404
    return response


def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response

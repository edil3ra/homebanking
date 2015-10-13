from . import api
from ..errors import ValidationError, bad_request, not_found


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(str(e))


@api.errorhandler(AttributeError)
def validation_error(e):
    return bad_request('no arguments provide')


@api.errorhandler(TypeError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')



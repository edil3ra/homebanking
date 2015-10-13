from flask import Blueprint, url_for
from flask import Blueprint, url_for, g
from ..decorators import json
from ..errors import ValidationError, bad_request, not_found

api = Blueprint('api', __name__)


@api.route('/')
@json
def index():
    return {'accounts_type_url': url_for('api.get_accounts_type', _external=True),
            'addresses_url': url_for('api.get_addresses', _external=True),
            'clients_url': url_for('api.get_clients',_external=True)}   



from . import errors, account_type, address, client


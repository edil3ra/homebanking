from flask import jsonify, abort, make_response, request
from ..models import db, AccountType
from ..decorators import json, paginate, all_items
from . import api


@api.route('/accounts_type/all/', methods=['GET'])
@all_items
def get_accounts_type_all():
    return AccountType.query


@api.route('/accounts_type/', methods=['GET'])
@paginate(AccountType)
def get_accounts_type():
    return AccountType.query


@api.route('/accounts_type/<int:id>/', methods=['GET'])
@json
def get_account_type(id):
    return AccountType.query.get_or_404(id)


@api.route('/accounts_type/', methods=['POST'])
@json
def new_account_type():
    account = AccountType().from_json(request.json)
    db.session.add(account)
    db.session.commit()
    return {}, 201, {'Location': account.get_url()}


@api.route('/accounts_type/<int:id>/', methods=['PUT'])
@json
def edit_account_type(id):
    account = AccountType.query.get_or_404(id)
    account.from_json(request.json)
    db.session.add(account)
    db.session.commit()
    return {}


@api.route('/accounts_type/<int:id>/', methods=['DELETE'])
@json
def delete_account_type(id):
    account = AccountType.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return {}


@api.route('/accounts_type/<int:id>/clients/all/', methods=['GET'])
@all_items
def get_account_type_clients_all(id):
    account_type = AccountType.query.get_or_404(id)
    return account_type.clients


@api.route('/accounts_type/<int:id>/clients/', methods=['GET'])
@paginate(AccountType)
def get_account_type_clients(id):
    account_type = AccountType.query.get_or_404(id)
    return account_type.clients

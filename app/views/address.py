from flask import jsonify, abort, make_response, request
from ..models import db, Address
from ..decorators import json, paginate, all_items
from . import api


@api.route('/addresses/all/', methods=['GET'])
@all_items
def get_address_all():
    return Address.query


@api.route('/addresses/', methods=['GET'])
@paginate(Address)
def get_addresses():
    return Address.query


@api.route('/addresses/<int:id>/', methods=['GET'])
@json
def get_address(id):
    return Address.query.get_or_404(id)


@api.route('/addresses/', methods=['POST'])
@json
def new_addresses():
    address = Address().from_json(request.json)
    db.session.add(address)
    db.session.commit()
    return {}, 201, {'Location': address.get_url()}


@api.route('/addresses/<int:id>/', methods=['PUT'])
@json
def edit_addresses(id):
    address = Address.query.get_or_404(id)
    address.from_json(request.json)
    db.session.add(address)
    db.session.commit()
    return {}


@api.route('/addresses/<int:id>/', methods=['DELETE'])
@json
def delete_addresses(id):
    address = Address.query.get_or_404(id)
    db.session.delete(address)
    db.session.commit()
    return {}


@api.route('/addresses/<int:id>/clients/all/', methods=['GET'])
@all_items
def get_addresses_clients_all(id):
    address = Address.query.get_or_404(id)
    return address.clients


@api.route('/addresses/<int:id>/clients/', methods=['GET'])
@paginate(Address)
def get_addresses_clients(id):
    address = Address.query.get_or_404(id)
    return address.clients


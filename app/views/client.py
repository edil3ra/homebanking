from flask import jsonify, abort, make_response, request
from ..models import db, Client
from ..decorators import json, paginate, all_items
from . import api


@api.route('/clients/all/', methods=['GET'])
@all_items
def get_clients_all():
    return Client.query


@api.route('/clients/', methods=['GET'])
@paginate(Client)
def get_clients():
    return Client.query


@api.route('/clients/<int:id>/', methods=['GET'])
@json
def get_client(id):
    return Client.query.get_or_404(id)


@api.route('/clients/', methods=['POST'])
@json
def new_client():
    client = Client().from_json(request.get_json(force=True))
    db.session.add(client)
    db.session.commit()
    return {}, 201, {'Location': client.get_url()}


@api.route('/clients/<int:id>/', methods=['PUT'])
@json
def edit_client(id):
    client = Client.query.get_or_404(id)
    client.from_json(request.json)
    db.session.add(client)
    db.session.commit()
    return {}


@api.route('/clients/<int:id>/', methods=['DELETE'])
@json
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return {}

# from flask.ext.sqlalchemy import SQLAlchemy
import unittest
from werkzeug.exceptions import BadRequest
from ..app import create_app
from ..app.models import db, Client, Address, AccountType
from ..app.errors import ValidationError
from .test_client import TestClient

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = TestClient(self.app)
        self.catalog = self._get_catalog()

        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        
        
    def _get_catalog(self):
        rv, json = self.client.get('/')
        return json

    
    def test_http_errors(self):
        # not found
        rv, json = self.client.get('/a-bad-url')
        self.assertTrue(rv.status_code == 404)
    

    def test_accounts_type(self):
        # get collection
        rv, json = self.client.get(self.catalog['accounts_type_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['accounts_type'] == [])

        # create new
        rv, json = self.client.post(self.catalog['accounts_type_url'],
                                    data={'value': 'credit'})
        self.assertTrue(rv.status_code == 201)
        credit_url = rv.headers['Location']

        # get
        rv, json = self.client.get(credit_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['value'] == 'credit')
        self.assertTrue(json['url'] == credit_url)

        # create new
        rv, json = self.client.post(self.catalog['accounts_type_url'],
                                    data={'value': 'deposit'})
        self.assertTrue(rv.status_code == 201)
        deposit_url = rv.headers['Location']

        # get
        rv, json = self.client.get(deposit_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['value'] == 'deposit')
        self.assertTrue(json['url'] == deposit_url)

        # bad request
        rv,json = self.client.post(self.catalog['accounts_type_url'], data=None)
        self.assertTrue(rv.status_code == 400)
        rv,json = self.client.post(self.catalog['accounts_type_url'], data={})
        self.assertTrue(rv.status_code == 400)
        self.assertRaises(ValidationError,
                          lambda: self.client.post(self.catalog['accounts_type_url'],
                                                   data={'fake': 'david'}))

        # modify
        rv, json = self.client.put(deposit_url, data={'value': 'saving'})
        self.assertTrue(rv.status_code == 200)

        # get
        rv, json = self.client.get(deposit_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['value'] == 'saving')

        # get collection
        rv, json = self.client.get(self.catalog['accounts_type_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(deposit_url in json['accounts_type'])
        self.assertTrue(credit_url in json['accounts_type'])
        self.assertTrue(len(json['accounts_type']) == 2)

        # delete
        rv, json = self.client.delete(deposit_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get(self.catalog['accounts_type_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertFalse(deposit_url in json['accounts_type'])
        self.assertTrue(credit_url in json['accounts_type'])
        self.assertTrue(len(json['accounts_type']) == 1)
        

    def test_address(self):
        # get collection
        rv, json = self.client.get(self.catalog['addresses_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [])

        # create new
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'fake addresses'})
        
        self.assertTrue(rv.status_code == 201)
        girona_url = rv.headers['Location']

        # get
        rv, json = self.client.get(girona_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['street'] == 'fake addresses')
        self.assertTrue(json['url'] == girona_url)

        self.assertTrue(json['city'] == None)
        self.assertTrue(json['region'] == None)
        self.assertTrue(json['country'] == None)
        self.assertTrue(json['postcode'] == None)
        self.assertTrue(json['longitude'] == None)
        self.assertTrue(json['latitude'] == None)
        
        # create new
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'P.O. Box 910, 1325 Congue Ave',
                                          'city': 'Baden',
                                          'region': 'Lower Austria',
                                          'country': 'Belgium',
                                          'postcode': '3314'})
        
        self.assertTrue(rv.status_code == 201)
        baden_url = rv.headers['Location']

        # get
        rv, json = self.client.get(baden_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['street'] == 'P.O. Box 910, 1325 Congue Ave')
        self.assertTrue(json['city'] == 'Baden')
        self.assertTrue(json['region'] == 'Lower Austria')
        self.assertTrue(json['country'] == 'Belgium')
        self.assertTrue(json['postcode'] == '3314')
        self.assertTrue(json['url'] == baden_url)

        # test longitude and latitude set correctly
        self.assertTrue(json['latitude'] == 26.5386725)
        self.assertTrue(json['longitude'] == -80.0907946)
        

        # bad request
        rv,json = self.client.post(self.catalog['addresses_url'], data=None)
        self.assertTrue(rv.status_code == 400)
        rv,json = self.client.post(self.catalog['addresses_url'], data={})
        self.assertTrue(rv.status_code == 400)
        self.assertRaises(ValidationError,
                          lambda: self.client.post(self.catalog['addresses_url'],
                                                   data={'fake': 'david'}))

        # modify
        rv, json = self.client.put(baden_url, data={'street': '204-2205 Vitae Road'})
        self.assertTrue(rv.status_code == 200)

        # get
        rv, json = self.client.get(baden_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['street'] == '204-2205 Vitae Road')

        # get collection
        rv, json = self.client.get(self.catalog['addresses_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(girona_url in json['addresses'])
        self.assertTrue(baden_url in json['addresses'])
        self.assertTrue(len(json['addresses']) == 2)

        # delete
        rv, json = self.client.delete(girona_url)
        self.assertTrue(rv.status_code == 200)

        # get collection
        rv, json = self.client.get(self.catalog['addresses_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertFalse(girona_url in json['addresses'])
        self.assertTrue(baden_url in json['addresses'])
        self.assertTrue(len(json['addresses']) == 1)



    def test_client(self):
        # get collection
        rv, json = self.client.get(self.catalog['clients_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['clients'] == [])


        # create new accounts_type
        rv, json = self.client.post(self.catalog['accounts_type_url'],
                                    data={'value': 'credit'})
        self.assertTrue(rv.status_code == 201)
        account_type_url = rv.headers['Location']
    
        rv, json = self.client.post(self.catalog['accounts_type_url'],
                                    data={'value': 'balance'})
        self.assertTrue(rv.status_code == 201)
        account_type_url_2 = rv.headers['Location']
        
        
        # create new addresses
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'P.O. Box 910, 1325 Congue Ave'})
        self.assertTrue(rv.status_code == 201)
        address_url = rv.headers['Location']
        
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': '204-2205 Vitae Road'})
        
        self.assertTrue(rv.status_code == 201)
        address_url_2 = rv.headers['Location']

        
        
        # create new client
        rv, json = self.client.post(self.catalog['clients_url'],
                                    data={"account_number": "CR1570510574788858783",
                                      	  "account_balance": 19855,
                                          "first_name": "Rogers",
                                          "birth_date": "08/02/2015",
                                          "address": address_url, 
                                          "account_type": account_type_url})
        
        self.assertTrue(rv.status_code == 201)
        client_url = rv.headers['Location']

        rv, json = self.client.post(self.catalog['clients_url'],
                                    data={"account_number": "SA8618280037617578604529",
                                      	  "account_balance": 24118,
                                          "first_name": "Cook",
                                          "birth_date": "10/28/2014",
                                          "address": address_url_2, 
                                          "account_type": account_type_url_2})
        
        self.assertTrue(rv.status_code == 201)
        client_url_2 = rv.headers['Location']

        
        
        # get client
        rv, json = self.client.get(client_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['url'] == client_url)
        self.assertTrue(json['account_number'] == 'CR1570510574788858783')
        self.assertTrue(json['account_balance'] == 19855)
        self.assertTrue(json['first_name'] == "Rogers")
        self.assertTrue(json['birth_date'] == "02/08/15")
        self.assertTrue(json['address'] == address_url)
        self.assertTrue(json['account_type'] == account_type_url)

        
        # get collection
        rv, json = self.client.get(self.catalog['clients_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(client_url in json['clients'])
        self.assertTrue(client_url_2 in json['clients'])
        self.assertTrue(len(json['clients']) == 2)

        
        # bad registrations
        rv,json = self.client.post(self.catalog['clients_url'],
                                   data=None)
        self.assertTrue(rv.status_code == 400)
        rv,json = self.client.post(self.catalog['clients_url'], data={})
        self.assertTrue(rv.status_code == 400)
        
        # missing address URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'address': address_url}))
        
        # missing account_type URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'account_type': account_type_url}))
        
        # address is not a URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'address': 'foo',
                                    'account_type': account_type_url}))
        
        # account_type is not a URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'address': address_url,
                                    'account_type': 'foo'}))
        
        # address is a not found URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'address': address_url + '1',
                                    'account_tye': account_type_url }))
        
        # account_tye is a not found URL
        self.assertRaises(ValidationError,
                          lambda: self.client.post(
                              self.catalog['clients_url'],
                              data={'address': address_url,
                                    'account_tye': account_type_url + '1' }))
        
        # modify
        rv, json = self.client.put(client_url, data={"account_number": "PT60735689954551948514718",
                                                     "account_balance": 53825,
                                                     "first_name": "Garner",
                                                     "birth_date": "10/28/2014",
                                                     "address": address_url_2,
                                                     "account_type": account_type_url_2})
        self.assertTrue(rv.status_code == 200)

        # get
        rv, json = self.client.get(client_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['url'] == client_url)
        self.assertTrue(json['account_number'] == 'PT60735689954551948514718')
        self.assertTrue(json['account_balance'] == 53825)
        self.assertTrue(json['first_name'] == "Garner")
        self.assertTrue(json['birth_date'] == "28/10/14")
        self.assertTrue(json['address'] == address_url_2)
        self.assertTrue(json['account_type'] == account_type_url_2)
        

        # get collection
        rv, json = self.client.get(self.catalog['clients_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(client_url in json['clients'])
        self.assertTrue(client_url_2 in json['clients'])
        self.assertTrue(len(json['clients']) == 2)
        
        # delete
        rv, json = self.client.delete(client_url)
        self.assertTrue(rv.status_code == 200)
        
        # get collection
        rv, json = self.client.get(self.catalog['clients_url'])
        self.assertTrue(rv.status_code == 200)
        self.assertFalse(client_url in json['clients'])
        self.assertTrue(client_url_2 in json['clients'])
        self.assertTrue(len(json['clients']) == 1)
        
        
    def test_expanded_collections(self):
        # create new addresses
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': '7367 Velit. Rd.'})
        
        self.assertTrue(rv.status_code == 201)
        url = rv.headers['Location']
        
        rv, json = self.client.get(self.catalog['addresses_url'] + "?expand=1")
        
        self.assertTrue(rv.status_code == 200)
        print(json)
        self.assertTrue(json['addresses'][0]['street'] == '7367 Velit. Rd.')
        self.assertTrue(json['addresses'][0]['url'] == url)
        
        
    def _create_test_addresses(self):
        # create several students
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'one'})
        self.assertTrue(rv.status_code == 201)
        one_url = rv.headers['Location']
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'two'})
        self.assertTrue(rv.status_code == 201)
        two_url = rv.headers['Location']
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'three'})
        self.assertTrue(rv.status_code == 201)
        three_url = rv.headers['Location']
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'four'})
        self.assertTrue(rv.status_code == 201)
        four_url = rv.headers['Location']
        rv, json = self.client.post(self.catalog['addresses_url'],
                                    data={'street': 'five'})
        self.assertTrue(rv.status_code == 201)
        five_url = rv.headers['Location']
        
        return [one_url, two_url, three_url, four_url, five_url]

    
    def test_filters(self):
        urls = self._create_test_addresses()
        
        # test various filter operators
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=street,eq,three')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[2]])

        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=street,ne,three&sort=id,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[0], urls[1], urls[3],
                                             urls[4]])

        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=id,le,2&sort=id,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[0], urls[1]])

        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=id,ge,2;id,lt,4&sort=id,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[1], urls[2]])

        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=street,in,three,five&sort=id,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[2], urls[4]])

        # bad operator is ignored
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=street,is,three,five')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['addresses']) == 5)

        # bad column street is ignored
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?filter=foo,in,three,five')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(len(json['addresses']) == 5)
        
        
    def test_sorting(self):
        urls = self._create_test_addresses()

        # sort ascending (implicit)
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?sort=street')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[4], urls[3], urls[0],
                                             urls[2], urls[1]])

        # sort ascending
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?sort=street,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[4], urls[3], urls[0],
                                             urls[2], urls[1]])

        # sort descending
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?sort=street,desc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['addresses'] == [urls[1], urls[2], urls[0],
                                             urls[3], urls[4]])
        

    def test_pagination(self):
        urls = self._create_test_addresses()

        # get collection in pages
        rv, json = self.client.get(self.catalog['addresses_url'] +
                                   '?page=1&per_page=2&sort=street,asc')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(urls[4] in json['addresses'])
        self.assertTrue(urls[3] in json['addresses'])
        self.assertTrue(len(json['addresses']) == 2)
        self.assertTrue('total' in json['meta'])
        self.assertTrue(json['meta']['total'] == 5)
        self.assertTrue('prev_url' in json['meta'])
        self.assertTrue(json['meta']['prev_url'] is None)
        first_url = json['meta']['first_url']
        last_url = json['meta']['last_url']
        next_url = json['meta']['next_url']

        rv, json = self.client.get(first_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(urls[4] in json['addresses'])
        self.assertTrue(urls[3] in json['addresses'])
        self.assertTrue(len(json['addresses']) == 2)

        rv, json = self.client.get(next_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(urls[0] in json['addresses'])
        self.assertTrue(urls[2] in json['addresses'])
        self.assertTrue(len(json['addresses']) == 2)
        next_url = json['meta']['next_url']

        rv, json = self.client.get(next_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(urls[1] in json['addresses'])
        self.assertTrue(len(json['addresses']) == 1)

        rv, json = self.client.get(last_url)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(urls[1] in json['addresses'])
        self.assertTrue(len(json['addresses']) == 1)

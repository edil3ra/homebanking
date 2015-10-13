from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Float
from werkzeug.exceptions import NotFound
from .errors import ValidationError
from flask import url_for, request
from datetime import date
import requests

API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


db = SQLAlchemy()

class Client(db.Model):
    __tablename__   = 'clients'
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(64), nullable=False)
    account_number  = Column(String(64), nullable=False)
    account_balance = Column(Float, nullable=False)
    birth_date      = Column(Date, nullable =False)
    account_type_id = Column('accounts_type_id', Integer,
                             db.ForeignKey('accounts_type.id'), nullable=False)
    address_id      = Column('addresses_id', Integer,
                             db.ForeignKey('addresses.id'), nullable=False)
    
    
    def get_url(self):
        return url_for('api.get_client', id=self.id, _external=True)
    
    
    def to_json(self):
        return {
            'url': self.get_url(),
            'first_name': self.first_name,
            'account_number': self.account_number,
            'account_balance': self.account_balance,
            'birth_date': self.birth_date.strftime('%d/%m/%y'),
            'account_type': url_for('api.get_account_type', id=self.account_type_id,
                                    _external=True),
            'address': url_for('api.get_address', id=self.address_id,
                               _external=True)
        }
    
    def string_date_to_python(self, str_date):
        month, day, year = map(int, str_date.split('/'))
        return date(year, month, day)
    
    def from_json(self, json):
        if request.method == 'POST':
            try:
                self.first_name = json['first_name']
                self.account_balance = json['account_balance']
                self.account_number = json['account_number']
                self.birth_date = self.string_date_to_python(json['birth_date'])
            except KeyError as e:
                raise ValidationError('Invalid address: missing ' + e.args[0])
            
            try:
                account_type_id = int(json['account_type'].split('/')[-2])
                self.account_type = AccountType.query.get_or_404(account_type_id)
            except (KeyError, NotFound):
                raise ValidationError('Invalid account_type URL')
            
            try:
                address_id = int(json['account_type'].split('/')[-2])
                self.address = Address.query.get_or_404(address_id)
            except (KeyError, NotFound):
                raise ValidationError('Invalid address URL')
            
            
        elif request.method == 'PUT':
            if json.get('first_name'):
                self.first_name = json.get('first_name')
            if json.get('account_number'):
                self.account_number = json.get('account_number')
            if json.get('account_balance'):
                self.account_balance = json.get('account_balance')
            if json.get('birth_date'):
                self.birth_date = self.string_date_to_python(json['birth_date'])
                
                
            if json.get('account_type'):
                try:
                    account_type_id = int(json['account_type'].split('/')[-2])
                    self.account_type = AccountType.query.get_or_404(account_type_id)
                except (KeyError, NotFound):
                    raise ValidationError('Invalid account_type URL')
            
            if json.get('address'):
                try:
                    address_id = int(json['address'].split('/')[-2])
                    self.address = Address.query.get_or_404(address_id)
                except (KeyError, NotFound):
                    raise ValidationError('Invalid address URL')
        return self
        
    
    def __repr__(self):
        return '\n'.join(['first_name: {}'.format(self.first_name),
                          'account_number: {}'.format(self.account_number),
                          'account_balance: {}'.format(self.account_balance),
                          'birth_date: {}'.format(self.birth_date.strftime('%d/%m/%y')),
                          'accounts_type_id: {}'.format(self.account_type_id),
                          'address_id: {}'.format(self.address_id)])


class Address(db.Model):
    __tablename__   = 'addresses'
    id        = Column(Integer, primary_key=True)
    street    = Column(String(256), nullable=False)
    city      = Column(String(256)) 
    region    = Column(String(256))
    country   = Column(String(256))
    postcode  = Column(String(256))
    latitude  = Column(Float)
    longitude = Column(Float)
    clients = db.relationship(Client,
                              backref=db.backref('address', lazy='joined'),
                              lazy='dynamic', cascade='all, delete-orphan', cascade_backrefs=False)

    # clients = db.relationship(Client,
    #                           backref=db.backref('address'),
    #                           cascade='all, delete-orphan')
    
    
    def __repr__(self):
        return '\n'.join(['street: {}'.format(self.street),
                          'city: {}'.format(self.city),
                          'region: {}'.format(self.region),
                          'country: {}'.format(self.country),
                          'postcode: {}'.format(self.postcode),
                          'longitude: {}'.format(self.longitude),
                          'latitude: {}'.format(self.latitude)
                      ])
    
    
    def get_url(self):
        return url_for('api.get_address', id=self.id, _external=True)

    
    def to_json(self):
        
        # optinal arguments
        # city = self.city if self.city else ''
        # region = self.region if self.region else ''
        # country = self.country if self.country else ''
        # postcode = self.postcode if self.postcode else ''
        # latitude = self.latitude if self.latitude else ''
        # longitude = self.longitude if self.longitude else ''


        city = self.city if self.city else None
        region = self.region if self.region else None
        country = self.country if self.country else None
        postcode = self.postcode if self.postcode else None
        latitude = self.latitude if self.latitude else None
        longitude = self.longitude if self.longitude else None
        
        return {
            'url': self.get_url(),
            'street': self.street,
            'city': city,
            'region': region,
            'country': country,
            'postcode': postcode,
            'latitude': latitude,
            'longitude': longitude,
            'clients': url_for('api.get_addresses_clients',
                                     id=self.id, _external=True)
        }
    
    def update_latitude_and_longitude(self, street):
        url       = '{}?address={}'.format(API_URL, street)
        result    = requests.get(url).json()
        status    = result['status']
        value     = result['results'][0] if len(result['results']) >= 1 else None
        
        if status != 'UNKNOWN_ERROR' and value:
            self.longitude = float(value['geometry']['location']['lng'])
            self.latitude  = float(value['geometry']['location']['lat'])
        else:
            self.latitude = None
            self.longitude = None
            
    
    def from_json(self, json):
        if request.method == 'POST':
            try:
                self.street = json['street']
            except KeyError as e:
                raise ValidationError('Invalid address: missing ' + e.args[0])
        elif request.method == 'PUT':
            if json.get('street'): self.street = json.get('street')
        
        # optional arguments
        # if json.get('city'): self.city = json.get('city')
        # if json.get('region'): self.region = json.get('region')
        # if json.get('country'): self.country = json.get('country')
        # if json.get('postcode'): self.postcode = json.get('postcode')
        
        self.city = json.get('city')
        self.region = json.get('region')
        self.country = json.get('country')
        self.postcode = json.get('postcode') 
        
        # self.city = json.get('city') if json.get('city') 
        # self.region = json.get('region') if json.get('region') 
        # self.country = json.get('country') if json.get('country') 
        # self.postcode = json.get('postcode') if json.get('postcode') 
        
        # update the longitude and latitude with the google api
        if json.get('street'):
            self.update_latitude_and_longitude(json.get('street'))
        
        return self


class AccountType(db.Model):
    __tablename__ = 'accounts_type'
    id      = Column(Integer, primary_key=True)
    value   = Column(String(256), unique=True)
    clients = db.relationship(Client,
                              backref=db.backref('account_type', lazy='joined'),
                              lazy='dynamic', cascade='all, delete-orphan', cascade_backrefs=False)

    # clients = db.relationship(Client,
    #                        backref=db.backref('account_type'),
    #                        cascade='all, delete-orphan')
    
    def __repr__(self):
        return '\n'.join(['value: {}'.format(self.value)])
    
    
    def get_url(self):
        return url_for('api.get_account_type', id=self.id, _external=True)
    
    
    def to_json(self):
        return {
            'url': self.get_url(),
            'value': self.value,
            'clients': url_for('api.get_account_type_clients',
                               id=self.id, _external=True)
        }
    
    def from_json(self, json):
        try:
            self.value = json['value']
        except KeyError as e:
            raise ValidationError('Invalid account type: missing ' + e.args[0])
        return self

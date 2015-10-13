import  os, sys
from app import db
from app.models import Client, Address, AccountType
import json
from datetime import date
import requests


API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def extract_data(filename):
    data = open(filename).read()
    return json.loads(data)



def set_clean_data(data):
    '''Create date object for the models,
       Set the longitude and latitude with the google api'''
    for client in data['client']:
        client_date = client['birth_date']
        month, day, year = map(int, client_date.split('/'))
        client['birth_date'] = date(year, month, day)
        
    
    for address in data['address']:
        street    = address['street']
        url       = '{}?address={}'.format(API_URL, street)
        result    = requests.get(url).json()
        status    = result['status']
        value     = result['results'][0] if len(result['results']) >= 1 else None
        
        if status != 'UNKNOWN_ERROR' and value:
            longitude = float(value['geometry']['location']['lng'])
            latitude  = float(value['geometry']['location']['lat'])
            address['longitude'] = longitude 
            address['latitude'] = latitude
            


def create_entries(data, ClassName):
    entries = [ClassName(**entry) for entry in data]
    db.session.add_all(entries)
    db.session.commit()



def empty_entries(className):
    db.session.query(className).delete()
    
 

def main():
    data_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.json')
    data = extract_data(data_filename)
    set_clean_data(data)
    
    empty_entries(Client)
    empty_entries(Address)
    empty_entries(AccountType)
    
    create_entries(data['client'], Client)
    create_entries(data['account_type'], AccountType)
    create_entries(data['address'], Address)
    
    
    
if __name__ == '__main__':
    main()

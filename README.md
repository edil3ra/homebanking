homebanking
===========

Requirements
------------

To install and run this application you need:

- Python 3.4 (2.7 not tested but probably work)


Installation
------------

The commands below install the application and its dependencies:

    $ git git@github.com:edil3ra/homebanking.git remplacer
    $ cd homebanking
    $ python -m venv venv
    $ source venv/bin/activate
    (venv) pip install -r requirements.txt
	python manage.py create_and_fill_database
	python manage.py runserver

all commands
    url_map             list all defined urls
    test                run unitest
    create_and_fill_database
                        create the database and fill the database with pregenerated
                        data
    runserver           Runs the Flask development server i.e. app.run()
    db                  Perform database migrations
    create_database     create the database
    fill_database       fill the database with pregenerated data
    shell               Runs a Python shell inside Flask application context.



Unit Tests
----------

	test_accounts_type (homebanking.tests.test_api.TestAPI) ... ok
	test_address (homebanking.tests.test_api.TestAPI) ... ok
	test_client (homebanking.tests.test_api.TestAPI) ... /home/vince/Envs/homebanking/lib/python3.4/site-packages/sqlalchemy/orm/unitofwork.py:235: SAWarning: Object of type <Client> not in session, add operation along 'AccountType.clients' will not proceed
	(orm_util.state_class_str(state), operation, prop))
	ok
	test_expanded_collections (homebanking.tests.test_api.TestAPI) ... ok
	test_filters (homebanking.tests.test_api.TestAPI) ... ok
	test_http_errors (homebanking.tests.test_api.TestAPI) ... ok
	test_pagination (homebanking.tests.test_api.TestAPI) ... ok
	test_sorting (homebanking.tests.test_api.TestAPI) ... ok

	----------------------------------------------------------------------
	Ran 8 tests in 5.566s

	OK


API Documentation
-----------------

General notes about this API:

- All resource representations are in JSON format.

The API supported by this application contains three top-level resource collections:

- *clients*: The collection of clients.
- *addresses*: The collection of addresses.
- *accounts_type*: The collection of accounts_type.

    http://localhost:5000/ version catalog:
    {
		accounts_type_url: "http://localhost:5000/accounts_type/",
		addresses_url: "http://localhost:5000/addresses/",
		clients_url: "http://localhost:5000/clients/"
	}
		
### Resource Collections

#### Filtering

Resource collections can be filtered by adding the `filter` argument to the query string of the collection resource URL. The format of a filter is as follows:

    [field_name],[operator],[value]

To build more complex queries multiple filters can be concatenated with a `;` separator. The operators can be `eq`, `ne`, `lt`, `le`, `gt`, `ge`, `like` and `in`. The `in` operator takes a list of values separated by commas, while all other operators take a single value

- Search by exact value: `filter=first_name,eq,Rogers`
- Search by range (all names that begin with "a"): `filter=name,ge,a;name,lt,b`
- Search in a set: `filter=name,in,Rogers,Cook`

Invalid filters are silently ignored.

Examples:
http://localhost:5000/addresses/?filter=street,eq,7367 Velit. Rd.
http://localhost:5000/addresses/?filter=street,ne,7367 Velit. Rd.&sort=id,asc
http://localhost:5000/addresses/?filter=id,le,2&sort=asc
http://localhost:5000/addresses/?filter=id,ge,2;id,lt,4&sort=id,asc 
http://localhost:5000/addresses/?filter=street,in,7367 Velit. Rd.,280-2426 Dictum Road&sort=id,asc


#### Resource Expansion

By default, when a collection of resources is returned, only their URLs are returned, as this maximizes caching efficiency. Example:

    {
        "clients": [
			"http://localhost:5000/clients/1/",
			"http://localhost:5000/clients/2/",
			"http://localhost:5000/clients/3/",
        ]
    }

However, in certain occasions it may be more convenient to obtain all the resources expanded. To request the resources in expanded form add `expand=1` to the query string of the collection resource URL. Example:

    {
		"clients": [
		   {
				account_balance: 19855,
				account_number: "CR1570510574788858783",
				account_type: "http://localhost:5000/accounts_type/1/",
				address: "http://localhost:5000/addresses/9/",
				birth_date: "02/08/15",
				first_name: "Rogers",
				url: "http://localhost:5000/clients/1/"
			},
			{
				account_balance: 24118,
				account_number: "SA8618280037617578604529",
				account_type: "http://localhost:5000/accounts_type/3/",
				address: "http://localhost:5000/addresses/2/",
				birth_date: "28/10/14",
				first_name: "Cook",
				url: "http://localhost:5000/clients/2/"
			},
			{
				account_balance: 53825,
				account_number: "PT60735689954551948514718",
				account_type: "http://localhost:5000/accounts_type/3/",
				address: "http://localhost:5000/addresses/8/",
				birth_date: "25/10/15",
				first_name: "Garner",
				url: "http://localhost:5000/clients/3/"
			}
	    ]
    }


#### Pagination

All requests to resource collection URLs are paginated, regardless of the client requesting so or not. The response from the server includes a `'meta'` key with information that is useful to navigate the pages of resources. Example:

    {
        "meta": {
			first_url: "http://localhost:5000/clients/?per_page=10&expand=1&page=1",
			last_url: "http://localhost:5000/clients/?per_page=10&expand=1&page=3",
			next_url: "http://localhost:5000/clients/?per_page=10&expand=1&page=2",
			page: 1,
			pages: 3,
			per_page: 10,
			prev_url: null,
			total: 30
        },
        "clients": [
            ...
        ]
    }

The `first_url`, `last_url`, `next_url` and `prev_url` fields contain the URLs to request other pages of the collection. When filtering, sorting and embedding options are used, these URLs contain the same options that were given for the current request.

The `page`, `pages`, `total` and `per_page` provide the current page, total number of pages, total number of items and items per page values respectively.

To request pagination settings that are different than the default, the `per_page` and `page` query string arguments must be added to the collection request URL


### Client Resource

    {
		account_balance: 19855,
		account_number: "CR1570510574788858783",
		account_type: "http://localhost:5000/accounts_type/1/",
		address: "http://localhost:5000/addresses/9/",
		birth_date: "02/08/15",
		first_name: "Rogers",
		url: "http://localhost:5000/clients/1/"
    }

The client resource supports `GET`, `POST`, `PUT` and `DELETE` methods to retrieve, create, edit and delete respectively. All fields are required for POST.

### address Resource

    {
		city: "Girona",
		clients: "http://localhost:5000/addresses/1/clients/",
		country: "Cocos (Keeling) Islands",
		latitude: -13.4156457,
		longitude: -76.14071009999999,
		postcode: "393051",
		region: "CA",
		street: "7367 Velit. Rd.",
		url: "http://localhost:5000/addresses/1/"
    }

The addresses resource supports `GET`, `POST`, `PUT` and `DELETE` methods to retrieve, create, edit and delete respectively. Only the street fields is required, if google api can retrieve the address it will automaticly set the longitude and latitude

### Account_type Resource

The account_type resource associates a student with a class. Below is the structure of this resource:

    {
		clients: "http://localhost:5000/accounts_type/1/clients/",
		url: "http://localhost:5000/accounts_type/1/",
		value: "credit"
    }

The account_type resource supports `GET`, `POST` and `DELETE` methods, to retrieve, create and delete respectively. 

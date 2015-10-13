#!/usr/bin/env python
from app import create_app, db
from app.models import Client, Address, AccountType
from flask import jsonify
from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime, date
from fake_data import fake_data


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return {'app': app, 'db': db, 'Client': Client, 'Address': Address,
            'AccountType': AccountType, 'jsonify': jsonify,
            'date': date, 'datetime': datetime}


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    '''Run the unit test'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def create_database():
    '''create the database'''
    db.drop_all()
    db.create_all()

    
@manager.command
def fill_database():
    '''fill the database with pregenerated data'''
    fake_data.main()

    
@manager.command
def create_and_fill_database():
    '''create the database and fill the database with pregenerated data'''
    create_database()
    fill_database()


@manager.command
def url_map():
    '''list all defined urls'''
    urls = list(app.url_map.iter_rules())
    for url in urls:
        print('{} {} -> {}'.format(url.rule, url.methods, url.endpoint))   


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v'])
    # call(['nosetests', '-v',
    #       '--with-coverage', '--cover-package=api', '--cover-branches',
    #       '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


        
if __name__ == '__main__':
    manager.run()

from flask import Flask
from config import config
# from .views import client
# from views import client
from .views import api
from .models import db
from .errors import not_found 


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    app.register_blueprint(api)

    @app.errorhandler(404)
    def not_found_error(e):
        return not_found('item not found')

    
    return app


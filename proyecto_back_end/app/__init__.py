from flask import Flask
from .config import Config
from .extensions import init_extensions
from flask_cors import CORS
from .routes.dashboard_api import dashboard_api


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.config['JSON_SORT_KEYS'] = False 

    init_extensions(app)
    app.register_blueprint(dashboard_api, url_prefix='/api/dashboard')

    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    print(app.url_map)
    return app
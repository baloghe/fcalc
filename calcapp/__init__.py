import os

from flask import Flask

class ProductionConfig:
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16) # 'dev'
    )
    # config
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # calculator instance
    from .models import Calculator
    
    # views
    from .views import bp
    app.register_blueprint(bp)
    app.calc = Calculator()

    return app
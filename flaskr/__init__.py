import os
from flask import Flask
import config


def create_app(test_config=None):
    """
    For more details, see http://flask.pocoo.org/docs/1.0/api/
    :param test_config:
    :return:
    """
    print("test_config", test_config)
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if "SECRET_KEY" in os.environ:
        # production
        app.config.from_mapping(
            SECRET_KEY=os.environ['SECRET_KEY'],
            MONGODB=os.environ['MONGODB']
        )

    elif test_config and 'TESTING' in test_config:
        # testing
        app.config.from_mapping(
            MONGODB=config.MONGODB
        )
    else:
        # development
        app.config.from_mapping(
            MONGODB=config.MONGODB
        )


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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

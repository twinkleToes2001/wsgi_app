"""The core application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


def create_app(dbms, user, password,
               host, port, database):
    """After create, run wsgi.py"""
    # Init app
    app = Flask(__name__)

    # Debug
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{dbms}://{user}:{password}@{host}:{port}/{database}' \
            .format(dbms=dbms, database=database,
                    user=user, password=password,
                    host=host, port=port)

    # Init database
    db.init_app(app)

    # Init marshmallow
    ma.init_app(app)

    with app.app_context():
        from . import routes
        # Create database tables for our data models
        db.create_all()

        return app

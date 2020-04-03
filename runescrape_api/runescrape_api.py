from flask import Flask
from .extensions import api
from .models.item import Item
import os


def create_app():
    app = Flask(__name__)
    db_connection = 'postgresql://{user}:{password}@{host}/postgres'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection.format(
        user=os.environ.get('DB_USER', 'postgres'), password=os.environ.get('DB_PASSWORD', 'insecure-password'), host=os.environ.get('DB_HOST', 'localhost'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register extensions
    # Order matters: Initialize SQLAlchemy before Marshmallow
    from .extensions import db, migrate, mm
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mm.init_app(app)

    return app

from flask import Flask
from .extensions import api
from .models.item import Item
import runescrape_api.views.item
import os
import logging
import sys


def create_app():
    app = Flask(__name__)
    db_connection = 'postgresql://{user}:{password}@{host}/postgres'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection.format(
        user=os.environ.get('DB_USER', 'postgres'), password=os.environ.get('DB_PASSWORD', 'insecure-password'), host=os.environ.get('DB_HOST', 'localhost'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    logging.basicConfig(stream=sys.stdout, level=os.environ.get("LOG_LEVEL", 20), format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Register extensions
    # Order matters: Initialize SQLAlchemy before Marshmallow
    from .extensions import db, migrate, mm
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mm.init_app(app)
    return app

from flask import request
from flask_restful import Resource, abort
from sqlalchemy import exc
from ..extensions import db
from ..models.item import Item, itemshistory_schema, itemhistory_schema
import logging


class ItemsHistory(Resource):
    def __init__(self):
        pass

    def get(self):
        items_response = Item.query.all()
        return itemshistory_schema.dump(items_response)

    def post(self):
        if request.json is None:
            abort(400)
        logging.debug(request.json)
        logging.info('{} item(s) posted'.format(len(request.json)))
        try:
            db.session.bulk_insert_mappings(Item, request.json)
        except exc.IntegrityError:
            logging.error('Duplicate key found!')
            db.session.rollback()
            abort(400, message='Duplicate key found!')
        db.session.commit()
        return {'ids': len(request.json)}


class ItemHistory(Resource):
    def __init__(self):
        pass

    def get(self, id):
        item_response = Item.query.filter_by(id=id).all()
        return itemhistory_schema.dump(item_response)

from flask import request
from flask_restful import Resource, abort
from sqlalchemy import exc
from ..extensions import db
from ..models.item import Item, itemshistory_schema, itemhistory_schema, items_schema
import logging
import datetime


class ItemsHistory(Resource):
    def __init__(self):
        pass

    def get(self):
        items_history_response = Item.query.all()
        return itemshistory_schema.dump(items_history_response)

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

    def get(self, id=None, name=None, history_length=None):

        def get_history(time_unit, quantity=1, id=None, name=None):
            if id is not None and name is None:
                item_history_response = Item.query.filter(Item.time >= datetime.datetime.now(
                ) - datetime.timedelta(**{time_unit: quantity})).filter_by(id=id).order_by(Item.time.asc()).all()
                return itemhistory_schema.dump(item_history_response)
            elif id is None and name is not None:
                item_history_response = Item.query.filter(Item.time >= datetime.datetime.now(
                ) - datetime.timedelta(**{time_unit: quantity})).filter_by(name=name).order_by(Item.time.asc()).all()
                return itemhistory_schema.dump(item_history_response)
            else:
                abort(500)

        if history_length is None:
            return get_history("days", id, name)

        if history_length[-1] != "s":
            history_length = history_length + "s"

        if history_length not in ("hours", "days", "weeks", "months"):
            abort(400)
        elif history_length == "months":
            return get_history("days", 30, id, name)
        else:
            return get_history(history_length, 1, id, name)


class Items(Resource):
    def __init__(self):
        pass

    def get(self):
        items_response = Item.query.filter(Item.time >= datetime.datetime.now(
        ) - datetime.timedelta(seconds=300)).order_by(Item.id.asc()).all()
        return items_schema.dump(items_response)

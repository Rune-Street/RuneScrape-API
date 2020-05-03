import datetime
import logging

from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from ..extensions import db, t
from ..models.item import (Item, Item_transaction, itemhistory_schema,
                           items_schema, itemshistory_schema)


class ItemsHistory(Resource):
    def __init__(self):
        pass

    def get(self):
        items_history_response = Item_transaction.query.all()
        return itemshistory_schema.dump(items_history_response)

    def post(self):
        if request.json is None:
            abort(400)
        logging.debug(request.json)
        logging.info('{} item(s) posted'.format(len(request.json)))

        # Insert into cache table
        cache_values = sorted([{'id': dict['id'], 'name': dict['name'], 'members': dict['members']} for dict in request.json], key=lambda x: x['id'])
        db.session.execute(insert(Item).values(cache_values).on_conflict_do_nothing())
        db.session.commit()

        try:
            db.session.bulk_insert_mappings(Item_transaction, request.json)
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
        @t.timer(name='1-Response')
        def get_history(time_unit, quantity=1, id=None, name=None):
            t.start('DB')
            if id is not None and name is None:
                item_history_response = Item_transaction.query.filter(Item_transaction.time >= datetime.datetime.now(
                ) - datetime.timedelta(**{time_unit: quantity})).filter_by(id=id).order_by(Item_transaction.time.asc()).all()
                t.stop('DB')
                t.start('Serialize')
                resp = itemhistory_schema.dump(item_history_response)
                t.stop('Serialize')
                return resp
            elif id is None and name is not None:
                item_history_response = Item_transaction.query.filter(Item_transaction.time >= datetime.datetime.now(
                ) - datetime.timedelta(**{time_unit: quantity})).filter_by(name=name).order_by(Item_transaction.time.asc()).all()
                t.stop('DB')
                t.start('Serialize')
                resp = itemhistory_schema.dump(item_history_response)
                t.stop('Serialize')
                return resp
            else:
                t.stop('DB')
                abort(500)

        if history_length is None or history_length == "view" or history_length == "view/":
            return get_history("days", 1, id, name)

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
        t.start('DB')
        items_response = Item.query.all()
        t.stop('DB')
        return items_schema.dump(items_response)


class PopulateItemBuyLimit(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req_url = 'https://oldschool.runescape.wiki/w/Grand_Exchange/Buying_limits'
        req = Request(url=req_url, headers=headers)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')

        body = soup.find(id="bodyContent")
        buy_limit_table = body.table.find("tbody")
        rows = buy_limit_table.find_all("tr")[1:]
        buy_limit_dict = {} 
        for row in rows:
            cells = row.find_all("td")
            buy_limit_dict[cells[0].a['title']] = cells[1].get_text()

        items = Item.query.all()

        for item in items:
            if item.name in buy_limit_dict:
                if int(item.buy_limit) != int(buy_limit_dict[item.name]):
                    item.buy_limit = buy_limit_dict[item.name]
                    db.session.commit()
                    print(item.name, item.buy_limit, buy_limit_dict[item.name])   

        return jsonify(items=[item.serialize() for item in items])
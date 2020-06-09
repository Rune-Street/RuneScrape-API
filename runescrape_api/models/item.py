from sqlalchemy.schema import Index
from sqlalchemy.sql.expression import text

from ..extensions import db, mm


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, nullable=False, unique=True,
                   primary_key=True, autoincrement=False)
    name = db.Column(db.String(), nullable=False, index=True)
    members = db.Column(db.Boolean, nullable=False)
    buy_limit = db.Column(db.Integer, nullable=False, server_default="-1")
    transactions = db.relationship(
        "Item_transaction", backref="item", lazy=True)


class Item_transaction(db.Model):
    __tablename__ = 'price_data'

    id = db.Column(db.Integer, db.ForeignKey(
        Item.id), nullable=False, primary_key=True, autoincrement=False)
    name = db.Column(db.String(), nullable=False)
    members = db.Column(db.Boolean, nullable=False)
    buy_average = db.Column(db.Integer, nullable=False)
    buy_quantity = db.Column(db.Integer, nullable=False)
    sell_average = db.Column(db.Integer, nullable=False)
    sell_quantity = db.Column(db.Integer, nullable=False)
    overall_average = db.Column(db.Integer, nullable=False)
    overall_quantity = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime(timezone=True),
                     server_default=text("date_trunc('hour', NOW()) + INTERVAL '5 min' * ROUND(date_part('minute', NOW()) / 5.0)"), nullable=False, primary_key=True)


db.Index('item_members_buylimit_idx', Item.members.desc(), Item.buy_limit)
db.Index('price_data_members_time_idx',
         Item_transaction.members.desc(), Item_transaction.time)

db.Index('price_data_name_time_idx',
         Item_transaction.name.desc(), Item_transaction.time)


class ItemSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


class ItemHistorySchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Item_transaction


itemhistory_schema = ItemHistorySchema(many=True)
itemshistory_schema = ItemHistorySchema(many=True)

# items_schema = ItemSchema(only=("id", "name"), many=True)
items_schema = ItemSchema(many=True)

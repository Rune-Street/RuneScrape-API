from sqlalchemy.sql.expression import text

from ..extensions import db, mm


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=False, unique=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    members = db.Column(db.Boolean, nullable=False)
    buy_limit = db.Column(db.Integer, nullable=False, server_default="-1")


class Item_transaction(db.Model):
    __tablename__ = 'price_data'

    # pk = db.Column(db.Integer, primary_key=True,
    #                autoincrement=True, unique=True, nullable=False)
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=False, unique=True)
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

    __table_args__ = (
        db.Index('price_data_members_time_idx', members.desc(), time),
        db.Index('price_data_name_time_idx', name.desc(), time)
    )


class ItemSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


class ItemHistorySchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Item_transaction


itemhistory_schema = ItemHistorySchema(many=True)
itemshistory_schema = ItemHistorySchema(many=True)

items_schema = ItemSchema(only=("id", "name"), many=True)

from sqlalchemy.sql.expression import text
from ..extensions import db, mm


class Item(db.Model):
    __tablename__ = 'price_data'

    # pk = db.Column(db.Integer, primary_key=True,
    #                autoincrement=True, unique=True, nullable=False)
    id = db.Column(db.Integer, nullable=False, primary_key=True)
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


class ItemHistorySchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


itemhistory_schema = ItemHistorySchema(many=True)
itemshistory_schema = ItemHistorySchema(many=True)

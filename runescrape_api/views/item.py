from ..extensions import api
from ..resources.item import ItemsHistory, ItemHistory

api.add_resource(ItemsHistory, "/items")
api.add_resource(ItemHistory, "/item/<int:item_id>")

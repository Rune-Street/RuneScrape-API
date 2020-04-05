from ..extensions import api
from ..resources.item import ItemsHistory, ItemHistory, Items

api.add_resource(ItemsHistory, "/items/history")
api.add_resource(ItemHistory, "/item/<int:id>/history")

api.add_resource(Items, "/items")

from ..extensions import api
from ..resources.item import ItemsHistory, ItemHistory, NamedItemHistory, Items

api.add_resource(ItemsHistory, "/items/history")
api.add_resource(ItemHistory, "/item/<int:id>/history")
api.add_resource(NamedItemHistory, "/item/<string:name>/history")

api.add_resource(Items, "/items")

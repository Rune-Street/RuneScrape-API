from ..extensions import api
from ..resources.item import ItemsHistory, ItemHistory, Items, PopulateItemBuyLimit

api.add_resource(ItemsHistory, "/items/history")
api.add_resource(ItemHistory, "/item/<int:id>/history", "/item/<int:id>/history/<string:history_length>", "/item/<string:name>/history", "/item/<string:name>/history/<string:history_length>")

api.add_resource(Items, "/items")

api.add_resource(PopulateItemBuyLimit, "/items/populateitembuylimit")
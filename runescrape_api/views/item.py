from ..extensions import api
from ..resources.item import (ItemHistory, Items, ItemsHistory,
                              PopulateItemBuyLimit)

api.add_resource(ItemsHistory, "/items/history")
api.add_resource(ItemHistory, "/item/<int:id>/history", "/item/<int:id>/history/<string:history_length>", "/item/<int:id>/history/<string:history_length>/<int:history_quantity>", "/item/<string:name>/history", "/item/<string:name>/history/<string:history_length>", "/item/<string:name>/history/<string:history_length>/<int:history_quantity>")

api.add_resource(Items, "/items")

api.add_resource(PopulateItemBuyLimit, "/items/buylimit")

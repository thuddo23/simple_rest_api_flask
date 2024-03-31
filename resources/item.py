import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        True
        # if item_id not in items:
        #     abort(404, message="Item not found")
        # return items[item_id]

    def delete(self, item_id):
        True
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        True
        # try:
        #     item = items[item_id]
        #     item |= item_data
        # except KeyError:
        #     abort(404, message="Item not found. n ")

@blp.route("/item")
class ItemList(MethodView):
    # @blp.response(200, ItemSchema(many=True))
    # def get(self):
    #     return {"items": list(items.values())}

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"f, An error occurred while inserting: {e}")
        return item
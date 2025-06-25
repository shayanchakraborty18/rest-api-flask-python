import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

# get all stores
@app.get('/stores')
def get_stores():
    return {"stores": list(stores.values())}, 200

# create store
@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201

# get single store
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        store = stores[store_id]
        return store, 200
    except KeyError:
        abort(404, message="store not found")

# get all items in a store
@app.get('/store/<string:store_id>/item')
def get_items_in_store(store_id):
    try:
        return {"items": stores[store_id]["items"]}, 200
    except KeyError:
        abort(404, message="store not found")

# create item
@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if ( "price" not in item_data or "store_id" not in item_data or "name" not in item_data ):
        abort( 400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item

# get items
@app.get("/item")
def get_all_items():
    try:
        return {"items": list(items.values())}, 200
    except KeyError:
        abort(404, message="items not found")


# get_item_in_store
@app.get("/item/<string:item_id>")
def get_item_in_store(item_id):
    try:
        item = items[item_id]
        return item, 200
    except KeyError:
        abort(404, message="item not found")

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request


app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]

# get all stores
@app.get('/stores')
def get_stores():
    return {"stores": stores}, 200

# create store
@app.post('/store')
def create_store():
    request_data = request.get_json()
    new_store = {
            "name": request_data['name'],
            "items": []
        }
    
    stores.append(new_store)
    return new_store, 201

# get single store
@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store, 200
    return {"message": "store not found"}, 404

# get all items in a store
@app.get('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return {"items": store['items']}, 200
    return {"message": "store not found"}, 404

# create item in a store
@app.post('/store/<string:name>/item')
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                "name": request_data['name'],
                "price": request_data['price']
            }
            store['items'].append(new_item)
            return new_item, 201
    return {"message": "store not found "}, 404

if __name__ == '__main__':
    app.run(debug=True)
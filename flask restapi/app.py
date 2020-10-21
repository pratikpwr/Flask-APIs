from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'MyStore',
        'items': [
            {
                'name': 'my product',
                'price': 299
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


# POST - receive data
# GET - send the data back

# GET /store - return list of all store
@app.route('/store', methods=['GET'])
def get_all_stores():
    return jsonify({'stores': stores})


# POST /store data: (name:) - create store with given name
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name> - give back store info
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify(store)
        else:
            return jsonify({'error': 'Store not Found'})


# POST store/<string:name>/item (name: , price:) - create item inside a store with the given name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if name == store['name']:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
        else:
            return jsonify({'error': 'Store not Found'})


# GET /store/<string:name>/ item - return all items inside the store
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item_in_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify({'items': store['items']})
        else:
            return jsonify({'error': 'Store not Found'})


app.run(port=5000)

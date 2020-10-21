from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authentication, identity

app = Flask(__name__)
app.secret_key = 'farCry'
api = Api(app)

jwt = JWT(app, authentication, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help='This Field can not be empty.'
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            return {'message': 'item {} does not exists.'.format(name)}, 400
        items.remove(item)
        return {'message': 'Item {} removed'.format(name)}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            new_item = {'name': name, 'price': data['price']}
            items.append(new_item)
            return new_item, 201
        items.remove(item)
        # item.update(data)
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(debug=True)

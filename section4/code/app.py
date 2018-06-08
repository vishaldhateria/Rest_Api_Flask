from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required

from security import authenticate, identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
 

items= []

#  inheritance from Resource class
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This Field cannot be left blank!"
                            )
    @jwt_required()
    def get(self,name):
        # to get only one item use next if next find no item will return None
       return {'item': next(filter(lambda x: x['name'] == name, items), None)}
    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message' : "An item with name '{}' already exists.".format(name)} , 400
        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return items, 201
    def delete(Self, name):
        global items
        items = list(filter(lambda x: x['name']!= name, items))
        return {'message': 'item deleted'}

    def put(self, name):
       
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = { 'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)

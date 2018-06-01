from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items= []

#  inheritance from Resource class
class Item(Resource):
    def get(self,name):
        item = next(filer(lambda x: x['name'] == name), None) #to get only one item use next if next find no item will return None
        return {'item': None}, 200 if item else 404 #404 popular status code
    def post(self,name):
        item = next(filer(lambda x: x['name'] == name), None) is not None:
            return {'message' : "An item with name '{}' already exists.".format(name)} , 400
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)

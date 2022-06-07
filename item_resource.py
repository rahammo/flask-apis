import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    table_name = "items"
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        request_item = Item.parser.parse_args()

        item = ItemModel(name, request_item['price'])
        
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM {table} WHERE name=?".format(table=self.table_name)
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'Item deleted'}

    def put(self, name):
        request_item = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, "price": request_item['price']}
        
        if item is None:
            try:
                updated_item.insert()
            except:
                {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()


class ItemList(Resource):
    table_name = "items"
    
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table}".format(table=self.table_name)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        
        return {"items": items}

    # def put(self, name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
        
    #     query = "SELECT * FROM {table}".format(table=self.table_name)
    #     if item is None:
    #         item = {'name': name, 'price': data['price']}
    #         items.append(item)
    #     else:
    #         item.update(data)
    #     return item

    #     connection.close()
        


# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')

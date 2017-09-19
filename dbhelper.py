import pymongo
from bson.objectid import ObjectId

DATABASE = "waitercaller"

class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client[DATABASE]

    def get_user(self, email):
        return self.db.users.find_one({"email" : email})

    def add_user(self, email, salt, hashed):
        self.db.users.insert({"email" : email, "salt" : salt,
        "hashed" : hashed})

    def add_table(self, number, owner):
        new_id = self.db.tables.insert({"number" : number, "owner" : owner})
        return new_id

    def update_table(self, _id, url):
        self.db.tables.update({"_id" : _id}, {"$set" : {"url" : url}})

    def get_tables(self, owner_id):
        return list(self.db.tables.find({"owner" : owner_id}))

    def get_table(self, table_id):
        return self.db.tables.find_one({"_id" : ObjectId(table_id)})

    def delete_table(self, table_id):
        self.db.tables.remove({"_id" : ObjectId(table_id)})

    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        try:
            self.db.requests.insert({"owner" : table['owner'],
            "table_number" : table['number'],
            "table_id" : table_id, "time" : time})
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def get_requests(self, owner_id):
        return list(self.db.requests.find({"owner" : owner_id}))

    def delete_request(self, request_id):
        self.db.requests.remove({"_id": ObjectId(request_id)})

    def add_categories(self, name):
        self.db.categories.insert({"categorie_name" : name})

    def add_menu_items(self, name, item, description, price):
        self.db.menu.insert({"categorie_name" : name, "item_name" : item, "description" : description, "price": price})

    def get_categories_name(self):
        categories = self.db.categories.find({}, {"_id" : 0, "categorie_name" : 1})
        return categories

    def get_menu_item_by_name(self, item):
        return self.db.menu.find_one({"item_name" : item})

    def get_menu(self):
        menu_all = self.db.menu.find({}, {"_id" : 0, "categorie_name" : 1, "item_name" : 1, "description" : 1, "price" : 1})
        return menu_all
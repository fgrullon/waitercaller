import pymongo

client = pymongo.MongoClient()
c = client['waitercaller']
print c.users.create_index("email", unique=True)
print c.requests.create_index("table_id", unique=True)
print c.categories.create_index("categorie_name", unique=True)
print c.menu.create_index("item_name", unique=True)
print c.orders.create_index("number", unique=True)
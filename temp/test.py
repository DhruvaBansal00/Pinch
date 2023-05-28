from tinydb import TinyDB, Query

db = TinyDB("test.json")
User = Query()

# db.insert({"int": 1, "char": "a"})
# random_str = "int"
db.remove(Query()["int"].exists())
db.insert({"int": 1, "char": "b"})
print(db.search((Query().int.exists())))

db.update({"int": 2}, Query().int.exists())
print(db.search((Query().int.exists())))

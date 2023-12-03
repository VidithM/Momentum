"Community DB methods"
from bson.objectid import ObjectId


def create_new_community(collection, data):
    "Add a community to the database"
    x = collection.insert_one(data)
    return str(x.inserted_id)


def query_community(collection, data):
    "Find a community"
    if data.get("rid"):
        data["_id"] = ObjectId(data["rid"])
        del data["rid"]
    x = collection.find(data)
    doclist = []
    for doc in x:
        print(doc)
        doclist.append(doc)
    return doclist


def delete_community(collection, data):
    "Delete Community"
    if data.get("rid"):
        data["_id"] = ObjectId(data["rid"])
        del data["rid"]
    collection.delete_one(data)


def update_community(collection, data):
    "Update community data"
    query = {"_id": ObjectId(data["rid"])}
    del data["rid"]
    data = {"$set": data}
    print(query)
    print(data)
    collection.update_one(query, data)
    return str(query["_id"])

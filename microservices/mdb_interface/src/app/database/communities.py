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
    if data.get("rids"):
        obids = []
        for item in data["rids"]["$in"]:
            obids.append(ObjectId(item))
        data["_id"] = {"$in": obids}
        del data["rids"]
    x = collection.find(data)
    doclist = []
    for doc in x:
        print(doc)
        doclist.append(doc)
        doc["rid"] = doc.pop("_id")
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

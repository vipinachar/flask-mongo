import pymongo 
from pymongo import MongoClient
from flask import Flask, jsonify, make_response, request
from bson import json_util 
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ana3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

app=Flask(__name__)

@app.route("/users", methods=["GET"])
def users():
    data = list()
    for user in collection.find({}):
        value = {
            "name":user["name"],
            "age":user["age"]
        }
        data.append(value)
    return jsonify(data)

@app.route("/user/<id>", methods={"GET"})
def detail_user(id):
    try:
        data = collection.find_one({"_id":ObjectId(id)})
        response = {
        "name":data["name"],
        "age":data["age"]
        }
        return jsonify(response)
    except:
        return jsonify("User with ID doesnt exist!"), 404
    


@app.route("/add", methods=["POST"])
def add_user():
    data = request.json
    user = {
        "name" : data["name"],
        "age" : data["age"]
    }
    collection.insert_one(user)
    return jsonify("user added", 200)

@app.route("/update/<id>", methods=["PUT"])
def update_user(id):
    data = request.json 
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":{"name": data["name"]}})
    return jsonify("updatred", 200)

@app.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        collection.delete_one({"_id":ObjectId(id)})
        return jsonify("User has been deleted")
    except:
        return jsonify("User with ID does not exist!!")

if __name__ == "__main__":
    app.run(debug=True)
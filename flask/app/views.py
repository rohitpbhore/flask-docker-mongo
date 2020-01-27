from app import app
import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# DB conf 
client = pymongo.MongoClient("mongodb://db:27017/")
db = client.tododb
db = client.users

# todo app routes
@app.route('/')
def todo():
    app_name = os.getenv("APP_NAME")
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items, app_name=app_name)

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)
    return redirect(url_for('todo'))

# Users CRUD APIs
@app.route('/users', methods=['GET'])
def get_users():
    return dumps(db.users.find())

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return dumps(db.users.find_one({'_id':ObjectId(id)}))

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify("User deleted successfully")
    response.status_code = 200
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        db.users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':{'name':_name, 'email':_email, 'password':_hashed_password}})
        response = jsonify("User updated successfully")
        response.status_code = 200
        return response
    else:
        return not_found()

@app.route('/users', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        db.users.insert({'name':_name, 'email':_email, 'password':_hashed_password})
        response = jsonify("User added successfully")
        response.status_code = 200
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response

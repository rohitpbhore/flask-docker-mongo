from app import app
import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# DB conf 
client = pymongo.MongoClient("mongodb://db:27017/")
tododb = client.tododb
db = client.users

# JWT Config
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "this-is-secret-key-can-change-it"

# todo app routes
@app.route('/')
def todo():
    app_name = os.getenv("APP_NAME")
    _items = tododb.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items, app_name=app_name)

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    tododb.tododb.insert(item_doc)
    return redirect(url_for('todo'))

# Users CRUD APIs
@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
    return dumps(db.users.find())

@app.route('/users/<id>', methods=['GET'])
@jwt_required
def get_user(id):
    return dumps(db.users.find_one({'_id':ObjectId(id)}))

@app.route('/users/<id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify("User deleted successfully")
    response.status_code = 200
    return response

@app.route('/users/<id>', methods=['PUT'])
@jwt_required
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

# Authentication
@app.route("/register", methods=["POST"])
def register():
    _json = request.json
    _email = _json['email']
    _name = _json['name']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        user = db.users.find_one({"email":_email})
        if user:
            return jsonify(message="User Already Exist"), 400
        else:
            _hashed_password = generate_password_hash(_password)
            user_info = dict(name=_name, email=_email, password=_hashed_password)
            db.users.insert(user_info)
            return jsonify(message="User added sucessfully"), 201
    else:
        return not_found()
    
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        _email = request.json["email"]
        _password = request.json["password"]
    else:
        _email = request.form["email"]
        _password = request.form["password"]

    user = db.users.find_one({"email": _email})
    if check_password_hash(user['password'], _password):
        access_token = create_access_token(identity=_email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 400

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response
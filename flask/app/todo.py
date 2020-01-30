from app import app
import os
from flask import Flask, redirect, url_for, request, render_template, jsonify, make_response
import pymongo

# DB conf 
client = pymongo.MongoClient(app.config["DB_HOST"])
tododb = client.tododb

@app.route("/query")
def query():
    if request.args:
        args = request.args
        return make_response(jsonify(query=args), 200)
    else:
        return jsonify(message="No query string received"), 400
    
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
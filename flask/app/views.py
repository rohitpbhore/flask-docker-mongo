from app import app
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

client = MongoClient("mongodb://db:27017/")
db = client.tododb

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

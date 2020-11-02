import json

from flask import Flask, session, redirect, url_for, request, abort, jsonify
from os import listdir
from os.path import join

from examples.no_db_example.mock_data_base import DataBase
from examples.no_db_example.models import Task
from examples.no_db_example.implementation import Implementation
from sync import Sync

app = Flask(__name__)
db = DataBase()

implementation = Implementation(db)
sync = Sync(implementation)


@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()

    if sync.is_valid(data):
        resp = sync.apply(data)
        return jsonify(resp)
    else:
        abort(400, sync.error_message)


@app.route('/list-db', methods=['GET'])
def list_db():
    return db.to_json()


@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.get_json()

    try:
        implementation.create(data['where'], json.dumps(data['data']))
    except (KeyError, TypeError):
        abort(400)

    return db.to_json()


@app.route('/delete-item', methods=['POST'])
def delete_item():
    data = request.get_json()

    try:
        implementation.delete(data['where'], data['id'])
    except (KeyError, TypeError):
        abort(400)

    return db.to_json()


def load_mock_data():
    path = 'example_data'
    folder = 'tasks'
    files = [join(path, folder, f) for f in listdir(join(path, folder))]

    tasks = []
    for file in files:
        f = open(file)
        tasks.append(Task.from_json(f.read()))
        f.close()

    db.add_table('tasks', tasks, Task)


if __name__ == '__main__':
    load_mock_data()
    app.run()

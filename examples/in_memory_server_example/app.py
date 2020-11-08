import json
from pprint import pprint

from mobync import Mobync

from flask import Flask, request, abort
from os import listdir
from os.path import join

from .mock_data_base import DataBase
from .models import Task, Diff
from .implementation import Implementation

app = Flask(__name__)
db = DataBase()

implementation = Implementation(db)
mobync = Mobync(implementation)


def get_owner_id_from_auth(token):
    return token


@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()
    pprint(data)

    if 'auth_token' not in data or 'diffs' not in data:
        abort(400)

    if 'logical_clock' not in data or 'diffs' not in data:
        abort(400)

    if 'diffs' not in data or 'diffs' not in data:
        abort(400)

    owner_id = get_owner_id_from_auth(data['auth_token'])
    res = ''

    try:
        res = mobync.apply(data['logical_clock'], data['diffs'], owner_id)
    except Exception as e:
        print(e)
        abort(400)

    pprint(res)

    return res


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
    # path = 'example_data'
    # folder = 'tasks'
    # files = [join(path, folder, f) for f in listdir(join(path, folder))]
    #
    # tasks = []
    # for file in files:
    #     f = open(file)
    #     tasks.append(Task.from_json(f.read()))
    #     f.close()

    db.add_table('tasks', [], Task)

    db.add_table('diffs', [], Diff)


if __name__ == '__main__':
    load_mock_data()
    app.run()

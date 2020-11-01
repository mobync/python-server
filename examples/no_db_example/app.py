from flask import Flask, session, redirect, url_for, request, abort, jsonify

from examples.no_db_example.mock_data_base import DataBase
from examples.no_db_example.models import Task
from sync import Sync
from examples.relational_db_example.implementation import Implementation
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

implementation = Implementation()
sync = Sync(implementation)

db = DataBase()


@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()

    if sync.is_valid(data):
        resp = sync.apply(data)
        return jsonify(resp)
    else:
        abort(400, sync.error_message)


@app.route('/list-tasks', methods=['GET'])
def list_tasks():
    resp = [task.to_dict() for task in db.get_table('tasks').list_table()]
    return jsonify(resp)


def load_mock_data():
    path = 'example_data'
    folder = 'tasks'
    files = [join(path, folder, f) for f in listdir(join(path, folder))]

    tasks = []
    for file in files:
        f = open(file)
        tasks.append(Task.from_json(f.read()))
        f.close()

    db.add_table('tasks', tasks)


if __name__ == '__main__':
    load_mock_data()
    app.run()

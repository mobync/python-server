<div align="center">
<p>
    <img width="80" src="https://raw.githubusercontent.com/mobync/python-server/master/examples/in_memory_server_example/example_data/images/logo-round.png">
</p>
<h1>The Mobync Python Lib</h1>
</div>

<div align="center">

[![Build Status](https://travis-ci.com/mobync/python-server.svg?branch=master)](https://travis-ci.com/mobync/python-server)

</div>

## Getting started

To use mobync, install the lib using pip:

```bash
pip install mobync
```

## Why use mobync

Mobync is a synchronization library aimed to facilitate online-offline sync between multiple devices for any frontend, any backend, and any database.

This repository implements mobync server in python, that means you can start using mobync sync on your python backend regardless of which backend you might be using, or even which database.

As mobync aims to provide online-offline sync between client and server, you will need to use mobync library both on your frontend application and backend.

Currently mobync has a client dart implementation and a server python implementation. That means you can plug mobync on your flutter app and provide online-offline synchronization.

### Online-offline synchronization

Online-offline synchronization means that your app will work seamlessly both online and offline, the user can use without noticing any difference, and you can implement your app not worrying about this when using mobync.

Mobync will automatically make your app store your changes locally on your app's database when the user has no connection, and automatically sync the data to the backend when the user has internet.

### Multiple devices support

your user can use your service across multiple devices at the same time and all will have them data synchronized with mobync.

Mobync implements a protocol that merges the user data and resolves conflicts. 

Mobync's protocol allows mobile applications running on distributed clients to get synced to a single source of truth to manage users’ data using any storage type. Mobync users Dart and Flutter to implement this protocol and communicate to a web server written in Python.

## Example projects

You can see some example projects using mobync on [Examples](https://github.com/mobync/python-server/tree/master/examples).

#### [Relational Database](https://github.com/mobync/python-server/tree/master/examples/relational_db_example)

An example project using mobync on a Flask backend using PostgreSQL database.

#### [In memory](https://github.com/mobync/python-server/tree/master/examples/in_memory_server_example)

An example project using mobync on a Flask backend using in memory mock database.

## Setting up mobync on your project

Mobync will work regardless of the database you use or the backend framework. All you need is to follow the steps.

### Create a Mobync diff model

Create the following model on your database:

```
id: str
owner: str
logical_clock: int
utc_timestamp: int
type: OperationType
model: str
json_data: str
```

That means, for example, that if your database is relational you should create a table with that structure.

### Implement a mobync Synchronizer child class

You will have to make an implementation of a child class from the Synchronizer abstract class.

Inside the class you need to provide the following methods implementation:

* read
* update
* create
* delete
* validate_create
* validate_update
* validate_delete

The read, update, create, and delete methods will create an interface to mobync interact with your database.

The validate_create, validate_update, and validate_delete will be authentication rules that you will define to validate an operation on your database based on the owner id of that operation and the data been modified. In a practical way this means, for example, that you will define if an operation is valid based on which user is operating and what data they are changing.

The following code is a possible way of implementing the methods:

```python
from mobync import ReadFilter, FilterType, Synchronizer

class Implementation(Synchronizer):

    def __init__(self, db: DataBase):
        self.db = db

    def read(self, where: str, filters: List[ReadFilter]) -> str:
        
        filtered_data = self.db.get_table(where)
        
        if filters:
            for f in filters:
                if f.filter_by == FilterType.equal:
                    filtered_data = filtered_data.select_equal(**{f.field_name: f.data})
                if f.filter_by == FilterType.majorOrEqual:
                    filtered_data = filtered_data.select_larger_or_equal(**{f.field_name: f.data})
        
        return filtered_data

    def update(self, where: str, data_json: str):
        data = json.loads(data_json)
        table = self.db.get_table(where)
        if table:
            id = data.pop('id')
            table.update_row(id, data)

    def create(self, where: str, data_json: str) -> str:
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def delete(self, where: str, data_json: str) -> None:
        data = json.loads(data_json)
        id = data.pop('id')

        table = self.db.get_table(where)
        if table:
            table.remove_row(id)

    def validate_create(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)

    def validate_update(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)

    def validate_delete(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)
```

### Implement a sync API endpoint 

```python
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
```


## Mobync 

Mobync currently doesn't support 

## Mobync Flutter Server Package

Using Mobync, you will wrap your database operations in such a way that any local data will get synced to a remote server, what will allow users from multiple clients to have an offline-online experience.



#### Postgres implementation

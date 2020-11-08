# mobync server in memory storage example

## Description

This example implements a Flask server that uses a mock database in memory.

## Goal

The goal is to show that mobync is capable of be run with any kind database even with a generic mock database.

## Setup

### Python virtual environment (optional)

We recommend you create a python virtual environment. Run:

```bash
python3 -m venv venv
```

### Install requirements

Run:

```bash
pip install -r requirements.txt
```

## Running

Run:

```bash
python app.py
```

Now the server will be running on your localhost

### Api

#### http://localhost:5000/sync

This is the sync endpoint, with it you can perform operations defined on mobync's protocol.

#### http://localhost:5000/list-db

With this endpoint you can list the current state of the mock database.

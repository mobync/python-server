# mobync server relational DB example

## Description

This example implements a Flask server that uses a relational database, in this case PostgreSQL.

## Goal

The goal is to show how to setup a relational database with mobync.

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

### API

#### http://localhost:5000/sync

This is the sync endpoint, with it you can perform operations defined on mobync's protocol.

#### http://localhost:5000/list-db

With this endpoint you can list the current state of the mock database.

## Troubleshooting

If error:

```
Is the server running locally and accepting
connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
```

run:

```
brew services stop postgresql
rm /usr/local/var/postgres/postmaster.pid # adjust path accordingly to your install
brew services start postgresql
```

if doesn't work, try:

```
rm -rf /usr/local/var/postgres && initdb /usr/local/var/postgres -E utf8
```


import os
from flask import Flask, session, redirect, url_for, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from mobync import Mobync
from examples.relational_db_example.implementation import Implementation

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

implementation = Implementation()
sync = Mobync(implementation)


@app.route('/sync', methods=['POST'])
def sync():
    data = request.get_json()

    if sync.is_valid(data):
        resp = sync.apply(data)
        return jsonify(resp)
    else:
        abort(400, sync.error_message)


def connect_db():
    try:
        connection = psycopg2.connect(user="sysadmin",
                                      password="pynative@#29",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres_db")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run()
    connect_db()

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymssql
import os

app = Flask(__name__)
CORS(app)

# Get DB connection info from environment
DB_SERVER = os.environ.get("DB_SERVER")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def get_connection():
    return pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/get_users", methods=["GET"])
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("SELECT id, username, email FROM Users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.json
        username = data.get("username")
        email = data.get("email")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Users (username, email) VALUES (%s, %s)",
            (username, email)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)})

# === Module Import Statements ===

import json
from flask import Flask, request, jsonify
import queries
import dbConnection
import passwordHash

# === Other Class Import Statements ===

# import rooms
# Where we have a .py file named "rooms.py" in the same folder.

# === Global Variables ===

# == Flask ==

app = Flask(__name__)

# == Application ==

conn = dbConnection.create_connection()

# === Routes ===

# == Post ==

@app.route('/post/register_user/', methods=["POST"])
def register_user():
    response = request.get_json()
    print_response_json(response)

    queries.insertUser(conn, response)

    return jsonify("Received post/register_user")

@app.route('/post/login_user/', methods=["POST"])
def login_user():
    response = request.get_json()
    json_as_dict = convert_json_to_dict(response)
    print(json_as_dict)

    user_profile = queries.getUserByUsername(conn, response)

    isPasswordValid = passwordHash.verifyPassword(user_profile["password"], json_as_dict["password"])
    print(isPasswordValid)

    if (isPasswordValid):
        return jsonify(user_profile["userID"])

@app.route('/post/reply/', methods=["POST"])
def post_reply():
    response = request.get_json()
    print_response_json(response)

    queries.insertReply(conn, response)

    return jsonify("Received post/reply")

@app.route('/post/category/', methods=["POST"])
def post_category():
    response = request.get_json()
    print_response_json(response)

    queries.insertCategory(conn, response)

    return jsonify("Received post/category")

@app.route('/post/board', methods=["POST"])
def post_board():
    response = request.get_json()
    print_response_json(response)

    queries.insertBoard(conn, response)

    return jsonify("Received post/board")

@app.route('/post/thread', methods=["POST"])
def post_thread():
    response = request.get_json()
    print_response_json(response)

    queries.insertThread(conn, response)

    return jsonify("Received post/thread")


@app.route('/get/threads/<id>', methods=["POST"])
def insert_reply(id):
    response = request.get_json()
    response["threadID"] = int(id)
    response = json.dumps(response)
    queries.insertReply(conn, response)
    conn.commit()
    return "reply post received"

@app.route('/get/boards/<id>', methods=["POST"])
def insert_thread(id):
    response = request.get_json()
    response["boardID"] = int(id)
    response = json.dumps(response)
    print(type(response))
    print(response)
    queries.insertThread(conn, response)
    conn.commit()
    return "thread post received"


# == Get ==

@app.route('/get/categories', methods=["GET"])
def get_categories():
    categories = queries.getCategoriesAsJsons(conn)

    return categories


@app.route('/get/boards/<id>', methods=["GET"])
def get_boards(id):
    boards = queries.getBoardsFromCategoryAsJsons(conn, id)

    return boards


@app.route('/get/threads/<id>', methods=["GET"])
def get_threads(id):
    threads = queries.getThreadsFromBoardAsJsons(conn, id)

    return threads


@app.route('/get/replies/<id>', methods=["GET"])
def get_replies(id):
    replies = queries.getRepliesFromThreadAsJsons(conn, id)
    return replies



# == Flask Helpers ==

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


# === Utility ===

def convert_json_to_dict(json_to_convert):
    json_as_str = json.dumps(json_to_convert)
    json_as_dict = json.loads(json_as_str)
    return json_as_dict

def print_response_json(json_to_print):
    json_as_dict = convert_json_to_dict(json_to_print)
    print(json_as_dict)


# === Main ===

if __name__ == '__main__':

    # app.run()
    app.run(debug=True)

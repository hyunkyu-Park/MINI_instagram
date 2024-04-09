import os
import hashlib
import pathlib
import uuid
import flask
from flask import abort, session
import minista
from minista.api.posts import check_auth


@minista.app.route('/api/v1/accounts/create/', methods=['POST'])
def create():
    """Display / route."""
    connection = minista.model.get_db()
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    fileobj = flask.request.files["file"]
    if not username or not password or not fullname \
            or not email or not fileobj:
        return flask.jsonify({'error': 'Bad Request'}), 400
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    result = cur.fetchone()
    if result:
        return flask.jsonify({'error': 'existing username'}), 409
    print("file obj", fileobj)
    filename = fileobj.filename
    print("file name", filename)
    uuidbasename = f"{uuid.uuid4().hex}{pathlib.Path(filename).suffix.lower()}"
    print("uuidbasename", uuidbasename)
    fileobj.save(minista.app.config["UPLOAD_FOLDER"]/uuidbasename)
    session["logged_in_user"] = username

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join(['sha512', salt, hash_obj.hexdigest()])
    cur = connection.execute(
        "INSERT INTO users (username, fullname, email, filename, password)\
            VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, uuidbasename, password_db_string)
    )
    return flask.jsonify({}), 200

@minista.app.route('/api/v1/accounts/login/', methods=['POST'])
def login():
    """Display / route."""
    connection = minista.model.get_db()
    username = flask.request.form.get('username')
    if username in session:
        target_url = "/"
        return flask.redirect(target_url)
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if not username or not password:
        return flask.jsonify({'error': 'Bad Request'}), 400
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    password_query = cur.fetchone()
    if not password_query:
        return flask.jsonify({'error': 'wrong password'}), 403
    else:
        currentpassword = password_query["password"]
        _, salt, current_password_hash = currentpassword.split("$")
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    if password_hash == current_password_hash:
        session["logged_in_user"] = username
    else:
        return flask.jsonify({'error': 'wrong password'}), 403
    return flask.jsonify({}), 200
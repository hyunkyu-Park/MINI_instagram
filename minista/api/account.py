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
    file = flask.request.files.get('file')
    if not username or not password or not fullname \
            or not email or not file:
        abort(400)
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    result = cur.fetchone()
    if result:
        abort(409)
    print("file saver")
    fileobj = flask.request.files["file"]
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
    return flask.redirect("/")
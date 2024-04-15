import os
import hashlib
import pathlib
import uuid
import flask
from flask import abort, session
import minista
from minista.api.posts import check_auth
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


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

#testing
@minista.app.route('/api/v1/accounts/generatePic/', methods=['POST'])
def generatePic_Create():
    connection = minista.model.get_db()
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')

    #Char for user profile
    first = username[0]

    randomR = random.randint(0, 255)
    randomG = random.randint(0, 255)
    randomC = random.randint(0, 255)

    # set img
    image_size = (200, 200)
    font_size = image_size[0] // 3 
    image = Image.new('RGB', image_size, color=(randomR, randomG, randomC))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default().font_variant(size=font_size)

    center_x = image_size[0]/4 + font_size/2
    center_y = image_size[1]/4
    print("centerx", center_x)
    print("centery", center_y)

    # draw text
    draw.text((center_x, center_y), first, fill=(255, 255, 255), font=font)

    # save img as a temp file
    temp_filename = f"{uuid.uuid4().hex}.png"
    print("temp_filename", temp_filename)
    image.save(minista.app.config["UPLOAD_FOLDER"]/temp_filename)

    # same step as normal create
    if not username or not password or not fullname \
            or not email:
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
    session["logged_in_user"] = username

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join(['sha512', salt, hash_obj.hexdigest()])
    cur = connection.execute(
        "INSERT INTO users (username, fullname, email, filename, password)\
            VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, temp_filename, password_db_string)
    )
    return flask.jsonify({}), 200

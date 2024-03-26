import hashlib
import flask
from flask import session
import minista
import pathlib
import uuid
import os
from minista.api.posts import check_auth

# current_directory = os.getcwd()
# UPLOADS_FOLDER = os.path.join(current_directory, 'var', 'uploads')

@minista.app.route('/api/v1/users/<user_url_slug>/')
def get_user_page(user_url_slug):
    """Display user information."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
    print("user_url_slug: ", user_url_slug)

    connection = minista.model.get_db()
    context = {
        "logname": None,
        "username": None,
        "full_name": None,
        "filename": None,
        "logname_follows_username": None,
        "following": None,
        "followers": None,
        "total_posts": None,
        "posts": [],
    }

    cur = connection.execute(
        "SELECT username, fullname, filename "
        "FROM users "
        "WHERE username = ? ",
        (user_url_slug,)
    )
    user_info = cur.fetchone()
    if not user_info:
        return flask.jsonify({"error": "User not found"}), 404

    context["logname"] = logname
    context["username"] = user_info["username"]
    context["full_name"] = user_info["fullname"]
    context["filename"] = f"/uploads/{user_info['filename']}"

    cur = connection.execute(
        "SELECT COUNT(*) as post_count "
        "FROM posts "
        "WHERE owner = ? ",
        (user_url_slug,)
    )
    num_posts = cur.fetchone()
    context["total_posts"] = num_posts["post_count"]

    cur = connection.execute(
        "SELECT COUNT(*) as followers_count "
        "FROM following "
        "WHERE username2 = ? ",
        (user_url_slug,)
    )
    numfollowers = cur.fetchone()
    context["followers"] = numfollowers["followers_count"]

    cur = connection.execute(
        "SELECT COUNT(*) as following_count "
        "FROM following "
        "WHERE username1 = ? ",
        (user_url_slug,)
    )
    numfollowing = cur.fetchone()
    context["following"] = numfollowing["following_count"]

    if logname:
        cur = connection.execute(
            "SELECT COUNT(*) as is_following "
            "FROM following "
            "WHERE username1 = ? AND username2 = ?",
            (logname, user_url_slug)
        )
        is_following = cur.fetchone()["is_following"]
        context["logname_follows_username"] = bool(is_following)

    cur = connection.execute(
        "SELECT postid, filename "
        "FROM posts "
        "WHERE owner = ?"
        "ORDER BY postid DESC",
        (user_url_slug,)
    )
    user_posts = cur.fetchall()
    post_ids = [post["postid"] for post in user_posts]
    filenames = [post["filename"] for post in user_posts]
    post_data = [
        {"postid": post_id, "filename": f"/uploads/{filename}"}
        for post_id, filename in zip(post_ids, filenames)
    ]
    context["posts"] = post_data

    return flask.jsonify(**context)

@minista.app.route('/api/v1/accounts/edit/')
def get_edit_page():
    """Display / route."""
    print("get_edit_page is called!")
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    context = {}
    connection = minista.model.get_db()
    cur = connection.execute(
        "SELECT username, fullname, email, filename "
        "FROM users "
        "WHERE username = ? ",
        (logname, )
    )
    user_info = cur.fetchone()
    context["logname"] = logname
    context["username"] = user_info["username"]
    context["full_name"] = user_info["fullname"]
    context["email"] = user_info["email"]
    context["user_photo_url"] = f"/uploads/{user_info['filename']}"

    return flask.jsonify(**context)

@minista.app.route('/api/v1/accounts/edit_account', methods=['POST'])
def edit_account():
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    username = logname

    if not fullname or not email:
        return flask.jsonify({"error": "No fullname or No email"}), 403
    if not flask.request.files["file"]:
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username = ? ",
            (fullname, email, username, )
        )
    else:
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = minista.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ? "
            "WHERE username = ? ",
            (fullname, email, uuid_basename, username, )
        )
    
    connection.commit()

    return flask.jsonify({}), 204

@minista.app.route('/api/v1/accounts/password/', methods=['GET'])
def get_password_page():
    """API endpoint to get password page data."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403

    context = {}
    context["logname"] = logname
    return flask.jsonify(**context)

@minista.app.route('/api/v1/accounts/password/', methods=['POST'])
def update_password():
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()
    
    password = flask.request.form.get('password')
    new_password1 = flask.request.form.get('new_password1')
    new_password2 = flask.request.form.get('new_password2')
    print("check", password)
    print("check", new_password1)
    print("check", new_password2)

    if not password or not new_password1 or not new_password2:
        return flask.jsonify({}), 400
    cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ? ",
            (logname, )
        )
    password_query = cur.fetchone()

    currentpassword = password_query["password"]
    _, salt, current_password_hash = currentpassword.split("$")
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    if password_hash != current_password_hash:
        return flask.jsonify({}), 403
    if new_password1 != new_password2:
        return flask.jsonify({}), 401
    # DONT FORGET TO HASH THE PASSWORD BEFORE STORE
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    cur = connection.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE username = ? ",
            (password_db_string, logname, )
    )

    connection.commit()

    return flask.jsonify({}), 204

@minista.app.route('/api/v1/accounts/delete/', methods=['DELETE'])
def delete_account():
    """Display / route."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    username = logname

    cur = connection.execute(
        "SELECT filename FROM posts WHERE owner = ?",
        (username, )
    )
    filenames = [result["filename"] for result in cur.fetchall()]
    directory = os.path.join(os.getcwd(), 'var', 'uploads')
    for filename in filenames:
        image_path = os.path.join(directory, filename)
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Error deleting image {filename}: {e}")

    cur1 = connection.execute(
        "SELECT filename FROM users WHERE username = ?",
        (username, )
    )
    filenames2 = [result["filename"] for result in cur1.fetchall()]
    directory = os.path.join(os.getcwd(), 'var', 'uploads')
    for filename in filenames2:
        image_path = os.path.join(directory, filename)
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Error deleting image {filename}: {e}")

    cur = connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username, )
    )
    session.clear()
    return flask.jsonify({}), 204

@minista.app.route('/api/v1/accounts/delete/', methods=['GET'])
def get_delete_page():
    """API endpoint to get delete page data."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403

    context = {}
    context["logname"] = logname
    return flask.jsonify(**context)

"""
minista index (main) view.

URLs include:
/
"""
import os
import hashlib
import pathlib
import uuid
import flask
from flask import abort, session
import arrow
import minista

app = flask.Flask(__name__)


@minista.app.route('/')
def show_index():
    """Display / route."""
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/users/<user_url_slug>/')
def show_user_page(user_url_slug):
    """Display / route."""
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/uploads/<filename>')
def upload_file(filename):
    """Display / route."""
    print("upload_file?")
    if "logged_in_user" not in session:
        abort(403)

    directory = minista.app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)
    directory = os.path.join(os.getcwd(), 'var', 'uploads')
    return flask.send_from_directory(directory, filename)

@minista.app.route('/users/<user_url_slug>/followers/')
def show_followers_page(user_url_slug):
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/users/<user_url_slug>/following/')
def show_following_page(user_url_slug):
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/explore/')
def show_explore():
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/posts/<postid_url_slug>/')
def show_post_page(postid_url_slug):
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/likes/', methods=['POST'])
def like_post():
    """Display / route."""
    print("this is never called??")
    # Connect to database
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        # Get values from the POST request form
        operation = flask.request.form.get('operation')
        postid = int(flask.request.form.get('postid'))
        target_url = flask.request.args.get("target", "/")
        logname = session["logged_in_user"]

        # Perform like or unlike operation
        # (In a real app, this is where you'd interact with your database)
        if operation == 'like':
            cur1 = connection.execute(
                "SELECT likeid "
                "FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname, postid)
            )
            result = cur1.fetchone()
            if result is None:
                connection.execute(
                    "INSERT INTO likes (owner, postid) VALUES (?, ?)",
                    (logname, postid)
                )
            else:
                abort(409)
        if operation == 'unlike':
            cur1 = connection.execute(
                "SELECT likeid "
                "FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname, postid)
            )
            result = cur1.fetchone()
            if result:
                connection.execute(
                    "DELETE FROM likes WHERE owner = ? AND postid = ? ",
                    (logname, postid)
                )
            else:
                abort(409)
        return flask.redirect(target_url)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/comments/', methods=['POST'])
def post_comments():
    """Display / route."""
    ""
    # Connect to database
    print("this is never called1??")
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        # Get values from the POST request form
        operation = flask.request.form.get('operation')
        postid = flask.request.form.get('postid')
        text = flask.request.form.get('text')
        target_url = flask.request.args.get("target", "/")
        commentid = flask.request.form.get('commentid')
        logname = session["logged_in_user"]

        if operation == "create":
            if text:
                cur = connection.execute(
                    "INSERT INTO comments \
                    (owner, postid, text) VALUES (?, ?, ?)",
                    (logname, postid, text)
                )
            else:
                abort(400)

        if operation == "delete":

            cur = connection.execute(
                "SELECT owner "
                "FROM comments "
                "WHERE commentid = ?",
                (commentid, )
            )
            owner = cur.fetchone()

            if not owner or owner["owner"] != logname:
                abort(403)
            else:
                cur = connection.execute(
                    "DELETE FROM comments WHERE commentid = ? ",
                    (commentid, )
                )
                connection.commit()
        return flask.redirect(target_url)
    target_url = "accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/accounts/', methods=['POST'])
def accounts_operations():
    """Display / route."""
    print("cccccccccc")
    operation = flask.request.form.get('operation')
    target_url = flask.request.args.get("target", "/")
    if operation == "login":
        login()
    elif operation == "create":
        create()
    # elif operation == "delete":
    #     delete()
    # elif operation == "edit_account":
    #     edit_account()
    # elif operation == "update_password":
    #     update_password()
    return flask.redirect(target_url)


@minista.app.route('/log/', methods=['POST'])
def login():
    """Display / route."""
    connection = minista.model.get_db()
    username = flask.request.form.get('username')
    target_url = flask.request.args.get("target", "/")
    if username in session:
        target_url = "/"
        return flask.redirect(target_url)
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if not username or not password:
        abort(400)
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    password_query = cur.fetchone()
    if not password_query:
        abort(403)
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
        abort(403)
    return flask.redirect(target_url)


@minista.app.route('/create/', methods=['POST'])
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


@minista.app.route('/accounts/delete/', methods=['POST'])
def delete():
    """Display / route."""
    connection = minista.model.get_db()
    # if not session["logged_in_user"]:
    if "logged_in_user" not in session:
        abort(403)
    username = session["logged_in_user"]

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
    target_url = flask.request.args.get("target", "/")
    return flask.redirect(target_url)

@minista.app.route('/accounts/login/')
def login_page():
    """Display / route."""
    context = {}
    return flask.render_template("login.html", **context)

@minista.app.route('/accounts/create/')
def create_page():
    """Display / route."""
    if "logged_in_user" in session:
        return flask.redirect("/accounts/edit/")
    context = {}
    return flask.render_template("create.html", **context)


@minista.app.route('/accounts/edit/')
def edit_page():
    """Display / route."""
    print("you should not see this message")
    context = {}
    connection = minista.model.get_db()
    cur = connection.execute(
        "SELECT username, fullname, email, filename "
        "FROM users "
        "WHERE username = ? ",
        (session["logged_in_user"], )
    )
    user_info = cur.fetchall()
    context["username"] = user_info[0]["username"]
    context["full_name"] = user_info[0]["fullname"]
    context["email"] = user_info[0]["email"]
    context["user_photo_url"] = user_info[0]["filename"]
    return flask.render_template("index.html", **context)

@minista.app.route('/accounts/delete/')
def delete_page():
    """Display / route."""
    print("this is never called2??")
    context = {}
    context["username"] = session["logged_in_user"]
    return flask.render_template("index.html", **context)

@minista.app.route('/accounts/password/')
def password_page():
    """Display / route."""
    print("this is never called3??")
    context = {}
    context["logname"] = session["logged_in_user"]
    return flask.render_template("index.html", **context)

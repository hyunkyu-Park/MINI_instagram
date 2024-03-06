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
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        cur = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 == ? ",
            (logname, )
        )
        post_owners = cur.fetchall()
        post_owners_li = []
        for post_owner in post_owners:
            post_owners_li.append(post_owner["username2"])
        post_owners_li.append(logname)

        posts = []
        for post_owner in post_owners_li:
            cur = connection.execute(
                "SELECT posts.postid, posts.filename, \
                    posts.owner, posts.created, \
                    COUNT(likes.postid) as like_count "
                "FROM posts "
                "LEFT JOIN likes ON posts.postid = likes.postid "
                "WHERE posts.owner == ? "
                "GROUP BY posts.postid "
                "ORDER BY posts.postid DESC",
                (post_owner, )
            )
            result = cur.fetchall()
            if result:
                for post in result:
                    cur = connection.execute(
                        "SELECT filename "
                        "FROM users "
                        "WHERE username == ? ",
                        (post_owner, )
                    )
                    user_image_result = cur.fetchone()
                    post["user_image"] = \
                        user_image_result["filename"] \
                        if user_image_result else ""

                    cur = connection.execute(
                        "SELECT commentid, text, owner "
                        "FROM comments "
                        "WHERE postid == ? "
                        "ORDER BY commentid ASC ",
                        (post["postid"], )
                    )
                    post["comments"] = cur.fetchall()
                    cur = connection.execute(
                        "SELECT COUNT(*) as is_like "
                        "FROM likes "
                        "WHERE owner = ? AND postid = ?",
                        (logname, post["postid"])
                    )
                    is_like = cur.fetchone()["is_like"]
                    post["is_like"] = bool(is_like)
                    posts.append(post)
        sorted_posts = sorted(posts, key=lambda x: x['postid'], reverse=True)
        for post in sorted_posts:
            real_time = arrow.get(post["created"])
            post["created"] = real_time.humanize()
        context = {}
        context["logname"] = logname
        context["posts"] = sorted_posts

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/users/<user_url_slug>/')
def show_user_page(user_url_slug):
    """Display / route."""
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context = {
            "logname": None,
            "username": None,
            "logname_follows_username": None,
            "full_name": None,
            "following": None,
            "followers": None,
            "total_posts": None,
            "posts": [],
        }

        cur = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username = ? ",
            (user_url_slug, )
        )
        user_info = cur.fetchone()
        if not user_info:
            abort(404)
        context["logname"] = logname
        cur = connection.execute(
            "SELECT username, fullname, filename "
            "FROM users "
            "WHERE username = ? ",
            (user_url_slug, )
        )
        user_info = cur.fetchall()
        context["username"] = user_info[0]["username"]
        context["full_name"] = user_info[0]["fullname"]
        context["filename"] = user_info[0]["filename"]

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
            "WHERE owner = ?",
            (user_url_slug, )
        )
        user_posts = cur.fetchall()
        post_ids = [post["postid"] for post in user_posts]
        filenames = [post["filename"] for post in user_posts]
        post_data = [
                    {"postid": post_id, "filename": filename}
                    for post_id, filename in zip(post_ids, filenames)
                ]
        context["posts"] = post_data

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/uploads/<filename>')
def upload_file(filename):
    """Display / route."""
    if "logged_in_user" not in session:
        abort(403)

    directory = minista.app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)
    directory = os.path.join(os.getcwd(), 'var', 'uploads')
    return flask.send_from_directory(directory, filename)


@minista.app.route('/accounts/auth/')
def get_auth():
    """Display / route."""
    if "logged_in_user" not in session:
        abort(403)
    return '', 200


@minista.app.route('/users/<user_url_slug>/followers/')
def show_followers_page(user_url_slug):
    """Display / route."""
    # Connect to database
    print("serverside followers page")
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context = {
            "logname": logname,
            "followers": []
        }

        owner = user_url_slug
        context['owner'] = owner
        cur = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username = ? ",
            (user_url_slug, )
        )
        result = cur.fetchone()
        if not result:
            abort(404)
        followingnames = []
        cur = connection.execute(
            "SELECT username1 "
            "FROM following "
            "WHERE username2 = ? ",
            (result["username"],)
        )
        results = cur.fetchall()
        for result in results:
            followingnames.append(result["username1"])

        filenames = []
        for follower in followingnames:
            cur = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = ? ",
                (follower,)
            )
            filenames.append(cur.fetchone()["filename"])

        relationships = []
        for follower in followingnames:
            cur = connection.execute(
                "SELECT COUNT(*) as is_following "
                "FROM following "
                "WHERE username1 = ? AND username2 = ? ",
                (logname, follower)
            )
            is_following = cur.fetchone()["is_following"]
            logname_follows_username = bool(is_following)
            relationships.append(logname_follows_username)

        context["followers"] = [
            {
                "username": follower,
                "user_img_url": filename,
                "logname_follows_username": isfollowing
            }
            for follower, filename, isfollowing in zip(
                followingnames,
                filenames,
                relationships
            )
        ]

        return flask.render_template("followers.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/users/<user_url_slug>/following/')
def show_following_page(user_url_slug):
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context = {
            "logname": logname,
            "following": []
        }

        owner = user_url_slug
        context['owner'] = owner

        cur = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username = ? ",
            (user_url_slug, )
        )
        result = cur.fetchone()
        if not result:
            abort(404)

        followingnames = []
        cur = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 = ? ",
            (result["username"],)
        )
        results = cur.fetchall()

        for result in results:
            followingnames.append(result["username2"])

        filenames = []
        for following in followingnames:
            cur = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = ? ",
                (following,)
            )
            filenames.append(cur.fetchone()["filename"])

        relationships = []
        for following in followingnames:
            cur = connection.execute(
                "SELECT COUNT(*) as is_following "
                "FROM following "
                "WHERE username1 = ? AND username2 = ? ",
                (logname, following)
            )
            is_following = cur.fetchone()["is_following"]
            logname_follows_username = bool(is_following)
            relationships.append(logname_follows_username)

        context["following"] = [
            {
                "username": following,
                "user_img_url": filename,
                "logname_follows_username": isfollowing
            }
            for following, filename, isfollowing in zip(
                followingnames,
                filenames,
                relationships
            )
        ]
        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/explore/')
def show_explore():
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context = {
            "logname": None,
            "not_following": []
        }
        context["logname"] = logname
        cur = connection.execute(
            "SELECT username "
            "FROM users "
            "WHERE username != ? AND username NOT IN ("
            "    SELECT username2 "
            "    FROM following "
            "    WHERE username1 == ?) ",
            (logname, logname)
        )

        result = cur.fetchall()
        not_following_users = []
        for res in result:
            not_following_users.append(res["username"])
        user_imgs = []
        for user in not_following_users:
            cur = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username == ? ",
                (user, )
            )
            user_img = cur.fetchone()
            user_imgs.append(user_img)
        context["not_following"] = [
            {
                "username": user,
                "user_img_url": user_img
            }
            for user, user_img in zip(
                not_following_users,
                user_imgs
            )
        ]

        return flask.render_template("explore.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/posts/<postid_url_slug>/')
def show_post_page(postid_url_slug):
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context = {}
        context["logname"] = logname
        context["postid"] = postid_url_slug
        context["is_like"] = False

        cur5 = connection.execute(
            "SELECT COUNT(*) as is_like "
            "FROM likes "
            "WHERE owner = ? AND postid = ?",
            (logname, postid_url_slug)
        )
        is_like = cur5.fetchone()["is_like"]
        context["is_like"] = bool(is_like)

        cur6 = connection.execute(
            "SELECT filename, owner, created "
            "FROM posts "
            "WHERE postid = ? ",
            (postid_url_slug,)
        )
        results = cur6.fetchone()
        owner = results["owner"]
        context["owner"] = results["owner"]
        context["img_url"] = results["filename"]
        read_time = arrow.get(results["created"])
        context["timestamp"] = read_time.humanize()

        cur7 = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (owner,)
        )
        results = cur7.fetchone()
        context["owner_img_url"] = results["filename"]
        cur8 = connection.execute(
            "SELECT COUNT(*) as like_count "
            "FROM likes "
            "WHERE postid = ? ",
            (postid_url_slug,)
        )
        results = cur8.fetchall()
        context["likes"] = results[0]["like_count"]

        cur9 = connection.execute(
            "SELECT owner, text, commentid "
            "FROM comments "
            "WHERE postid = ? ",
            (postid_url_slug,)
        )
        results = cur9.fetchall()
        context["comments"] = results
        # owner, post_id, owner_img_url, likes, img_url, comments
        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)


@minista.app.route('/likes/', methods=['POST'])
def like_post():
    """Display / route."""
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
    # Connect to database
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


@minista.app.route('/posts/', methods=['POST'])
def post_posts():
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()
    if "logged_in_user" in session:
        # Get values from the POST request form
        logname = session["logged_in_user"]
        operation = flask.request.form.get('operation')
        redirect = f"/users/{logname}/"
        target_url = flask.request.args.get("target", redirect)

        if operation == "create":
            # Unpack flask object
            fileobj = flask.request.files["file"]
            filename = fileobj.filename
            if not filename:
                abort(400)
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"
            # Save to disk
            fileobj.save(minista.app.config["UPLOAD_FOLDER"]/uuid_basename)

            cur = connection.execute(
                " INSERT INTO posts(filename, owner) "
                "VALUES (?, ?) ",
                (uuid_basename, logname)
            )
        elif operation == "delete":

            cur = connection.execute(
                "SELECT owner "
                "FROM posts "
                "WHERE postid = ? ",
                (int(flask.request.form.get('postid')), )
            )

            if logname != cur.fetchone()["owner"]:
                abort(403)
            else:
                cur = connection.execute(
                    "SELECT filename "
                    "FROM posts "
                    "WHERE postid = ?",
                    (int(flask.request.form.get('postid')), )
                )
                filenames = [result["filename"] for result in cur.fetchall()]
                directory = os.path.join(os.getcwd(), 'var', 'uploads')
                for filename in filenames:
                    image_path = os.path.join(directory, filename)
                    try:
                        os.remove(image_path)
                    except OSError as e:
                        print(f"Error deleting image {filename}: {e}")

                cur = connection.execute(
                    "DELETE "
                    "FROM posts "
                    "WHERE postid = ? ",
                    (int(flask.request.form.get('postid')), )
                )
                connection.commit()

                cur = connection.execute(
                    "DELETE "
                    "FROM comments "
                    "WHERE postid = ? ",
                    (int(flask.request.form.get('postid')), )
                )
                connection.commit()

                cur = connection.execute(
                    "DELETE "
                    "FROM likes "
                    "WHERE postid = ? ",
                    (int(flask.request.form.get('postid')), )
                )
                connection.commit()

        return flask.redirect(target_url)
    return flask.redirect("/accounts/login/")


# @minista.app.route('/following/', methods=['POST'])
# def post_following():
#     """Display / route."""
#     # Connect to database
#     connection = minista.model.get_db()
#     if "logged_in_user" in session:
#         # Get values from the POST request form
#         logname = session["logged_in_user"]
#         operation = flask.request.form.get('operation')
#         username = flask.request.form.get('username')
#         target_url = flask.request.args.get("target", "/")

#         if operation == "follow":
#             cur = connection.execute(
#                 "SELECT username1, username2 "
#                 "FROM following "
#                 "WHERE username1 = ? AND username2 = ? ",
#                 (logname, username, )
#             )
#             result = cur.fetchone()
#             if result:
#                 abort(409)
#             else:
#                 cur = connection.execute(
#                     "INSERT INTO following (username1, username2) \
#                     VALUES (?, ?)",
#                     (logname, username, )
#                 )
#         if operation == "unfollow":
#             cur = connection.execute(
#                 "SELECT username1, username2 "
#                 "FROM following "
#                 "WHERE username1 = ? AND username2 = ? ",
#                 (logname, username, )
#             )
#             result = cur.fetchone()
#             if result:
#                 cur = connection.execute(
#                     "DELETE "
#                     "FROM following "
#                     "WHERE username1 = ? AND username2 = ? ",
#                     (logname, username, )
#                 )
#             else:
#                 abort(409)
#         return flask.redirect(target_url)
#     target_url = "/accounts/login/"
#     return flask.redirect(target_url)


@minista.app.route('/accounts/', methods=['POST'])
def accounts_operations():
    """Display / route."""
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
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    uuidbasename = f"{uuid.uuid4().hex}{pathlib.Path(filename).suffix.lower()}"
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
        (username, fullname, email, filename, password_db_string)
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


# @minista.app.route('/accounts/edit_account', methods=['POST'])
# def edit_account():
#     """Display / route."""
#     connection = minista.model.get_db()
#     if "logged_in_user" not in session:
#         abort(403)
#     fullname = flask.request.form.get('fullname')
#     email = flask.request.form.get('email')
#     username = session["logged_in_user"]
#     if not fullname or not email:
#         abort(400)
#     if not flask.request.files["file"]:
#         connection.execute(
#             "UPDATE users "
#             "SET fullname = ?, email = ? "
#             "WHERE username = ? ",
#             (fullname, email, username, )
#         )
#     else:
#         fileobj = flask.request.files["file"]
#         filename = fileobj.filename
#         stem = uuid.uuid4().hex
#         suffix = pathlib.Path(filename).suffix.lower()
#         uuid_basename = f"{stem}{suffix}"
#         path = minista.app.config["UPLOAD_FOLDER"]/uuid_basename
#         fileobj.save(path)
#         connection.execute(
#             "UPDATE users "
#             "SET fullname = ?, email = ?, filename = ? "
#             "WHERE username = ? ",
#             (fullname, email, uuid_basename, username, )
#         )
#     target_url = flask.request.args.get("target", "/")
#     return flask.redirect(target_url)


# @minista.app.route('/accounts/password/', methods=['POST'])
# def update_password():
#     """Display / route."""
#     connection = minista.model.get_db()
#     if "logged_in_user" not in session:
#         abort(403)
#     print("not first abort")
#     password = flask.request.form.get('password')
#     new_password1 = flask.request.form.get('new_password1')
#     new_password2 = flask.request.form.get('new_password2')

#     if not password or not new_password1 or not new_password2:
#         abort(400)
#     cur = connection.execute(
#             "SELECT password "
#             "FROM users "
#             "WHERE username = ? ",
#             (session["logged_in_user"], )
#         )
#     password_query = cur.fetchone()

#     currentpassword = password_query["password"]
#     _, salt, current_password_hash = currentpassword.split("$")
#     algorithm = 'sha512'
#     hash_obj = hashlib.new(algorithm)
#     password_salted = salt + password
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     if password_hash != current_password_hash:
#         abort(403)
#     if new_password1 != new_password2:
#         abort(401)
#     # DONT FORGET TO HASH THE PASSWORD BEFORE STORE
#     hash_obj = hashlib.new(algorithm)
#     password_salted = salt + new_password1
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     password_db_string = "$".join([algorithm, salt, password_hash])

#     cur = connection.execute(
#             "UPDATE users "
#             "SET password = ? "
#             "WHERE username = ? ",
#             (password_db_string, session["logged_in_user"], )
#     )
#     return flask.redirect(flask.request.args.get("target", "/"))


@minista.app.route('/accounts/login/')
def login_page():
    """Display / route."""
    context = {}
    return flask.render_template("login.html", **context)


@minista.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Display / route."""
    session.clear()
    return flask.redirect("/accounts/login/")


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
    context = {}
    context["username"] = session["logged_in_user"]
    return flask.render_template("index.html", **context)


@minista.app.route('/accounts/password/')
def password_page():
    """Display / route."""
    print("Should not see this!")
    context = {}
    context["logname"] = session["logged_in_user"]
    return flask.render_template("index.html", **context)

"""REST API for posts."""
import hashlib
import flask
from flask import session
import minista
import pathlib
import uuid


def check_auth():
    """Chekcking Auth."""
    if "logged_in_user" in session:
        return session["logged_in_user"]
    if flask.request.authorization is not None:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
    else:
        return None

    connection = minista.model.get_db()
    cur_password = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    password_query = cur_password.fetchone()
    if not password_query:
        return None

    current_pass = password_query["password"]
    _, salt, curr_pass_hash = current_pass.split("$")
    algorithm = 'sha512'
    hash_now = hashlib.new(algorithm)
    password_salted = salt + password
    hash_now.update(password_salted.encode('utf-8'))
    pass_hash = hash_now.hexdigest()

    if pass_hash != curr_pass_hash:
        return None

    return username


@minista.app.route('/api/v1/')
def get_services():
    """Return post on postid."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@minista.app.route('/api/v1/posts/')
def get_posts():
    """Get the 10 newest posts."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    postid_lte = flask.request.args.get("postid_lte", type=int)
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    current_url = flask.request.full_path
    current_url = current_url.rstrip('?')
    offset = page * size
    if size <= 0 or page < 0:
        flask.abort(400, "Bad Request")

    context = {
            "results": [],
            "url": None,
            "next": "",
        }

    connection = minista.model.get_db()
    if postid_lte is None:
        cur1 = connection.execute(
            "WITH FollowingPosts AS ( "
            "SELECT p.postid "
            "FROM posts p "
            "WHERE p.owner = ? "
            "UNION "
            "SELECT p.postid "
            "FROM posts p "
            "JOIN following f ON p.owner = f.username2 "
            "WHERE f.username1 = ? ) "
            "SELECT fp.postid "
            "FROM FollowingPosts fp "
            "ORDER BY fp.postid DESC "
            "LIMIT ? OFFSET ?",
            (logname, logname, size, offset, )
        )
        first_row = cur1.fetchall()
        postid_lte = first_row[0]["postid"]

    cur = connection.execute(
        "WITH FollowingPosts AS ( "
        "SELECT p.postid "
        "FROM posts p "
        "WHERE p.owner = ? "
        "UNION "
        "SELECT p.postid "
        "FROM posts p "
        "JOIN following f ON p.owner = f.username2 "
        "WHERE f.username1 = ? ) "
        "SELECT fp.postid "
        "FROM FollowingPosts fp "
        "WHERE fp.postid <= ? "
        "ORDER BY fp.postid DESC "
        "LIMIT ? OFFSET ? ",
        (logname, logname, postid_lte, size, offset, )
    )
    posts = cur.fetchall()
    new_size = len(posts)

    if new_size == size:
        results = [
            {
                "postid": post["postid"],
                "url": f"/api/v1/posts/{post['postid']}/"
            }
            for post in posts
        ]
        next_url = (
            f"/api/v1/posts/?size={size}&"
            f"page={page + 1}&"
            f"postid_lte={postid_lte}"
        )
        context = {
            "results": results,
            "url": current_url,
            "next": next_url,
        }
    else:
        results = [
            {
                "postid": post["postid"],
                "url": f"/api/v1/posts/{post['postid']}/"
            }
            for post in posts
        ]
        context = {
            "results": results,
            "url": current_url,
            "next": "",
        }
    return flask.jsonify(**context)


@minista.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Get Post."""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    cur_post_check = connection.execute(
        "SELECT COUNT(*) FROM posts WHERE postid = ?",
        (postid_url_slug,)
    )
    
    if cur_post_check.fetchone()["COUNT(*)"] == 0:
        return flask.jsonify({'error': 'Post not found'}), 404

    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE postid = ? ",
        (postid_url_slug, )
    )
    comments = []
    for comment in cur.fetchall():
        comment["lognameOwnsThis"] = comment["owner"] == logname
        comment["ownerShowUrl"] = f"/users/{comment['owner']}/"
        comment["url"] = f"/api/v1/comments/{comment['commentid']}/"
        comments.append(comment)

    cur_post = connection.execute(
        "SELECT p.owner, p.filename AS p_f, u.filename AS u_f, p.created "
        "FROM posts AS p "
        "JOIN users AS u ON p.owner = u.username "
        "WHERE p.postid = ?",
        (postid_url_slug,)
    )
    post_info = cur_post.fetchone()

    cur_likes = connection.execute(
        "SELECT COUNT(*) AS num_likes, "
        "       EXISTS(SELECT 1 FROM likes "
        "              WHERE postid = ? AND owner = ?) AS logname_likes_this, "
        "       (SELECT likeid FROM likes "
        "        WHERE postid = ? AND owner = ?) AS likeid "
        "FROM likes "
        "WHERE postid = ?",
        (postid_url_slug, logname, postid_url_slug, logname, postid_url_slug)
    )
    likes_info = cur_likes.fetchone()
    likes = {
        "numLikes": likes_info["num_likes"],
        "lognameLikesThis": likes_info["logname_likes_this"] == 1,
        "url": (
            f"/api/v1/likes/{likes_info['likeid']}/"
            if likes_info["likeid"]
            else None
        )
    }

    lognameOwnsPost = False
    if logname == post_info['owner']:
        lognameOwnsPost = True

    context = {
        "lognameOwnsPost": lognameOwnsPost,
        "owner": post_info['owner'],
        "ownerImgUrl": f"/uploads/{post_info['u_f']}",
        "ownerShowUrl": f"/users/{post_info['owner']}/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": f"/api/v1/posts/{postid_url_slug}/",
        "likes": likes,
        "created": post_info["created"],
        "imgUrl": f"/uploads/{post_info['p_f']}",
        "comments": comments,
        "comments_url": f"/api/v1/comments/?postid={postid_url_slug}",
    }

    return flask.jsonify(**context)


@minista.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """Create like."""
    owner = check_auth()
    if owner is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    postid = flask.request.args.get('postid')
    connection = minista.model.get_db()

    cur_post = connection.execute(
        "SELECT COUNT(*) FROM posts WHERE postid = ?",
        (postid,)
    )
    post_exists = cur_post.fetchone()
    if post_exists is not None:
        post_exists = True
    else:
        return flask.jsonify({"error": "Post ID not found"}), 404

    cur_like = connection.execute(
        "SELECT likeid FROM likes WHERE postid = ?",
        (postid,)
    )
    existing_like = cur_like.fetchone()

    if existing_like is not None:
        likeid = existing_like['likeid']
        url = f"/api/v1/likes/{likeid}/"
        return flask.jsonify({"likeid": likeid, "url": url}), 200

    cur_insert = connection.execute(
        "INSERT INTO likes (postid, owner) VALUES (?, ?)",
        (postid, owner, )
    )
    new_likeid = cur_insert.lastrowid
    url = f"/api/v1/likes/{new_likeid}/"
    return flask.jsonify({"likeid": new_likeid, "url": url}), 201


@minista.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete like."""
    owner = check_auth()
    if owner is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    # Check if the likeid exists
    cur_like = connection.execute(
        "SELECT owner FROM likes WHERE likeid = ?",
        (likeid,)
    )
    existing_like = cur_like.fetchone()

    if existing_like is None:
        return flask.jsonify({"error": "Like ID not found"}), 404

    if existing_like['owner'] != owner:
        return flask.jsonify({"error": "No permission to delete like"}), 403

    connection.execute(
        "DELETE FROM likes WHERE likeid = ?",
        (likeid,)
    )

    return flask.jsonify({}), 204


@minista.app.route('/api/v1/comments/', methods=['POST'])
def add_comment():
    """Add comment."""
    postid = flask.request.args.get('postid')
    text = flask.request.json.get('text')
    owner = check_auth()
    if owner is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    cur_error_check = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    if cur_error_check.fetchone() is None:
        return flask.jsonify({"error": "Post ID not found"}), 404

    cur_insert = connection.execute(
        "INSERT into comments (postid, text, owner) VALUES (?, ?, ?) ",
        (postid, text, owner)
    )
    comment_id = cur_insert.lastrowid

    comment_data = {
        "commentid": comment_id,
        "lognameOwnsThis": True,
        "owner": owner,
        "ownerShowUrl": f"/users/{owner}/",
        "text": text,
        "url": f"/api/v1/comments/{comment_id}/"
    }

    return flask.jsonify(comment_data), 201


@minista.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete comment."""
    owner = check_auth()
    if owner is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    cur_comment = connection.execute(
        "SELECT owner FROM comments WHERE commentid = ?",
        (commentid,)
    )
    existing_comment = cur_comment.fetchone()

    if existing_comment is None:
        return flask.jsonify({"error": "Comment ID not found"}), 404

    if existing_comment['owner'] != owner:
        return flask.jsonify({"error": "No permission to delete comment"}), 403

    connection.execute(
        "DELETE FROM comments WHERE commentid = ?",
        (commentid,)
    )

    return flask.jsonify({}), 204



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
        "WHERE owner = ?",
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
    """Display / route."""
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


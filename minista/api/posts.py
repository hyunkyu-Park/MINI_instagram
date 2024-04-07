"""REST API for posts."""
import hashlib
import flask
from flask import session
import minista
import pathlib
import uuid
import os

app = flask.Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True

@minista.app.route('/accounts/auth/')
def aws_auth():
    """AWS Auth."""
    if "logged_in_user" not in session:
        flask.abort(403)
    return ""
    

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
    print("sec check",app.config['SESSION_COOKIE_SECURE'])
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
        return flask.jsonify({}), 400

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
        first_row = cur1.fetchone()
        if first_row:
            postid_lte = first_row["postid"]
            print("postid_lte:", postid_lte)

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
    if post_exists is None:
        return flask.jsonify({"error": "Post ID not found"}), 404

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
    print("deleted id", likeid)

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

@minista.app.route('/api/v1/accounts/logout/', methods=['POST'])
def logout():
    session.clear()
    return flask.jsonify({}), 204

@minista.app.route('/api/v1/posts/', methods=['POST'])
def post_posts():
    """Display / route."""
    print("post_posts!")
    # Connect to database
    connection = minista.model.get_db()
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
    # Get values from the POST request form
    operation = flask.request.form.get('operation')
    redirect = f"/users/{logname}/"
    target_url = flask.request.args.get("target", redirect)

    if operation == "create":
        # Unpack flask object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        if not filename:
            return flask.jsonify({}), 400
        
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
        post_id = int(flask.request.form.get('postid'))

        cur = connection.execute(
            "SELECT owner, filename FROM posts WHERE postid = ?",
            (post_id,)
        )
        
        post_info = cur.fetchone()

        if not post_info or logname != post_info["owner"]:
            return flask.jsonify({}), 400

        filenames = [post_info["filename"]]
        directory = os.path.join(os.getcwd(), 'var', 'uploads')

        for filename in filenames:
            image_path = os.path.join(directory, filename)
            try:
                os.remove(image_path)
            except OSError as e:
                print(f"Error deleting image {filename}: {e}")

        connection.execute("DELETE FROM posts WHERE postid = ?", (post_id,))
        connection.execute("DELETE FROM comments WHERE postid = ?", (post_id,))
        connection.execute("DELETE FROM likes WHERE postid = ?", (post_id,))
        connection.commit()

        print("committed!")

    return flask.redirect(target_url)

@minista.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['DELETE'])
def delete_post(postid_url_slug):
    """Delete post."""

    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    connection = minista.model.get_db()

    redirect = f"/users/{logname}/"
    target_url = flask.request.args.get("target", redirect)

    cur_comment = connection.execute(
        "SELECT owner FROM posts WHERE postid = ?",
        (postid_url_slug,)
    )
    existing_post = cur_comment.fetchone()

    if existing_post is None:
        return flask.jsonify({"error": "Post ID not found"}), 404

    if existing_post['owner'] != logname:
        return flask.jsonify({"error": "No permission to delete post"}), 403

    connection.execute(
        "DELETE FROM posts WHERE postid = ?",
        (postid_url_slug,)
    )
    connection.commit()

    return flask.jsonify({}), 204

@minista.app.route('/api/v1/explore/')
def get_explore():

    connection = minista.model.get_db()
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
    context = {
        "logname": logname,
        "not_following": []
    }

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
        user_imgs.append(user_img["filename"])
    context["not_following"] = [
        {
            "username": user,
            "user_img_url": f"/uploads/{user_img}"
        }
        for user, user_img in zip(
            not_following_users,
            user_imgs
        )
    ]

    return flask.jsonify(**context), 200


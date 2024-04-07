import flask
import minista
from minista.api.posts import check_auth


@minista.app.route('/api/v1/users/<user_url_slug>/followers/', methods=['GET'])
def get_followers_page(user_url_slug):
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()

    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
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
        return flask.jsonify({'error': 'Post not found'}), 404
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
            "user_img_url": f"/uploads/{filename}",
            "logname_follows_username": isfollowing
        }
        for follower, filename, isfollowing in zip(
            followingnames,
            filenames,
            relationships
        )
    ]

    return flask.jsonify(**context)

@minista.app.route('/api/v1/following/', methods=['POST'])
def post_following():
    """Follow or unfollow a user."""
    # Connect to database
    connection = minista.model.get_db()

    # Check if the user is logged in
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403

    # Get values from the POST request form
    operation = flask.request.form.get('operation')
    username = flask.request.form.get('username')

    # Follow operation
    if operation == "follow":
        cur = connection.execute(
            "SELECT username1, username2 "
            "FROM following "
            "WHERE username1 = ? AND username2 = ? ",
            (logname, username, )
        )
        result = cur.fetchone()
        if result:
            return flask.jsonify({'error': 'Already following'}), 404
        else:
            cur = connection.execute(
                "INSERT INTO following (username1, username2) VALUES (?, ?)",
                (logname, username, )
            )

    # Unfollow operation
    elif operation == "unfollow":
        cur = connection.execute(
            "SELECT username1, username2 "
            "FROM following "
            "WHERE username1 = ? AND username2 = ? ",
            (logname, username, )
        )
        result = cur.fetchone()
        if result:
            cur = connection.execute(
                "DELETE FROM following WHERE username1 = ? AND username2 = ? ",
                (logname, username, )
            )
        else:
            return flask.jsonify({'error': 'Not following'}), 404

    return flask.jsonify({}), 200

@minista.app.route('/api/v1/users/<user_url_slug>/following/', methods=['GET'])
def get_following_page(user_url_slug):
    """Display / route."""
    # Connect to database
    connection = minista.model.get_db()

    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
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
        return flask.jsonify({'error': 'Post not found'}), 404
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
            "user_img_url": f"/uploads/{filename}",
            "logname_follows_username": isfollowing
        }
        for following, filename, isfollowing in zip(
            followingnames,
            filenames,
            relationships
        )
    ]

    return flask.jsonify(**context), 200
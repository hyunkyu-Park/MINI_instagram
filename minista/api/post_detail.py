"""REST API for post_detail."""
import arrow
import flask
import minista
from posts import check_auth

@minista.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post_detail(postid_url_slug):
    """Display post information"""
    logname = check_auth()
    if logname is None:
        return flask.jsonify({"error": "Invalid Auth"}), 403
    
    connection = minista.model.get_db()
    
    context = {
        "logname": logname,
        "postid": postid_url_slug,
        "is_like": False,
        "owner": None,
        "img_url": None,
        "timestamp": None,
        "owner_img_url": None,
        "likes": 0,
        "comments": [],
    }

    if logname:
        cur_like = connection.execute(
            "SELECT COUNT(*) as is_like "
            "FROM likes "
            "WHERE owner = ? AND postid = ?",
            (logname, postid_url_slug)
        )
        is_like = cur_like.fetchone()["is_like"]
        context["is_like"] = bool(is_like)

    cur_post = connection.execute(
        "SELECT filename, owner, created "
        "FROM posts "
        "WHERE postid = ? ",
        (postid_url_slug,)
    )
    post_results = cur_post.fetchone()
    if not post_results:
        return flask.jsonify({"error": "Post not found"}), 404

    context["owner"] = post_results["owner"]
    context["img_url"] = post_results["filename"]
    read_time = arrow.get(post_results["created"])
    context["timestamp"] = read_time.humanize()

    cur_owner = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (context["owner"],)
    )
    owner_results = cur_owner.fetchone()
    context["owner_img_url"] = owner_results["filename"]

    cur_likes = connection.execute(
        "SELECT COUNT(*) as like_count "
        "FROM likes "
        "WHERE postid = ? ",
        (postid_url_slug,)
    )
    likes_results = cur_likes.fetchone()
    context["likes"] = likes_results["like_count"]

    cur_comments = connection.execute(
        "SELECT owner, text, commentid "
        "FROM comments "
        "WHERE postid = ? ",
        (postid_url_slug,)
    )
    comments_results = cur_comments.fetchall()
    context["comments"] = comments_results

    return flask.jsonify(**context)


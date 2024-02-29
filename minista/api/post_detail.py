"""REST API for post_detail."""
import flask
import minista
from minista.api.posts import check_auth

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
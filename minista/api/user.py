# """REST API for users."""
# import flask
# import minista
# from minista.api.posts import check_auth

# @minista.app.route('/api/v1/users/<user_url_slug>/')
# def get_user_page(user_url_slug):
#     """Display user information."""
#     logname = check_auth()
#     if logname is None:
#         return flask.jsonify({"error": "Invalid Auth"}), 403
    
#     print("user_url_slug: ", user_url_slug)

#     connection = minista.model.get_db()
#     context = {
#         "logname": None,
#         "username": None,
#         "full_name": None,
#         "filename": None,
#         "logname_follows_username": None,
#         "following": None,
#         "followers": None,
#         "total_posts": None,
#         "posts": [],
#     }

#     cur = connection.execute(
#         "SELECT username, fullname, filename "
#         "FROM users "
#         "WHERE username = ? ",
#         (user_url_slug,)
#     )
#     user_info = cur.fetchone()
#     if not user_info:
#         return flask.jsonify({"error": "User not found"}), 404

#     context["logname"] = logname
#     context["username"] = user_info["username"]
#     context["full_name"] = user_info["fullname"]
#     context["filename"] = f"/uploads/{user_info['filename']}"

#     cur = connection.execute(
#         "SELECT COUNT(*) as post_count "
#         "FROM posts "
#         "WHERE owner = ? ",
#         (user_url_slug,)
#     )
#     num_posts = cur.fetchone()
#     context["total_posts"] = num_posts["post_count"]

#     cur = connection.execute(
#         "SELECT COUNT(*) as followers_count "
#         "FROM following "
#         "WHERE username2 = ? ",
#         (user_url_slug,)
#     )
#     numfollowers = cur.fetchone()
#     context["followers"] = numfollowers["followers_count"]

#     cur = connection.execute(
#         "SELECT COUNT(*) as following_count "
#         "FROM following "
#         "WHERE username1 = ? ",
#         (user_url_slug,)
#     )
#     numfollowing = cur.fetchone()
#     context["following"] = numfollowing["following_count"]

#     if logname:
#         cur = connection.execute(
#             "SELECT COUNT(*) as is_following "
#             "FROM following "
#             "WHERE username1 = ? AND username2 = ?",
#             (logname, user_url_slug)
#         )
#         is_following = cur.fetchone()["is_following"]
#         context["logname_follows_username"] = bool(is_following)

#     cur = connection.execute(
#         "SELECT postid, filename "
#         "FROM posts "
#         "WHERE owner = ?",
#         (user_url_slug,)
#     )
#     user_posts = cur.fetchall()
#     post_ids = [post["postid"] for post in user_posts]
#     filenames = [post["filename"] for post in user_posts]
#     post_data = [
#         {"postid": post_id, "filename": f"/uploads/{filename}"}
#         for post_id, filename in zip(post_ids, filenames)
#     ]
#     context["posts"] = post_data

#     return flask.jsonify(**context)


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
    # file_path = os.path.join(directory, filename)
    # if not os.path.isfile(file_path):
    #     abort(404)
    # directory = os.path.join(os.getcwd(), 'var', 'uploads')
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

@minista.app.route('/accounts/login/')
def login_page():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)

@minista.app.route('/accounts/create/')
def create_page():
    """Display / route."""
    if "logged_in_user" in session:
        return flask.redirect("/accounts/edit/")
    context = {}
    return flask.render_template("index.html", **context)

@minista.app.route('/accounts/edit/')
def edit_page():
    """Display / route."""
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/accounts/delete/')
def delete_page():
    """Display / route."""
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

@minista.app.route('/accounts/password/')
def password_page():
    """Display / route."""
    if "logged_in_user" in session:
        logname = session["logged_in_user"]
        context ={"logname": logname}

        return flask.render_template("index.html", **context)
    target_url = "/accounts/login/"
    return flask.redirect(target_url)

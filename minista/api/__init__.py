"""minista REST API."""

from minista.api.posts import *
from minista.api.user_account import *
from minista.api.follower_following import *
from minista.api.account import *

app = flask.Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
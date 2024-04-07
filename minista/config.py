"""minista development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'GP\xf4q[J\xd3\xddv\xf2\xcd\xda0CA\x96D\xb4\xdb~\x86h\x13'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
minista_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = minista_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/minista.sqlite3
DATABASE_FILENAME = minista_ROOT/'var'/'minista.sqlite3'

# Turn on cookie secure option
SESSION_COOKIE_SECURE = True
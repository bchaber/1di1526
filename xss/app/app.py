from os import getenv
from flask import Flask
from .dao import dao
from .bp import bp
from .api import api
from .auth import auth
from .posts import posts

PREFIX = getenv('PREFIX','')
app = Flask(__name__)
app.secret_key = 'deadbeef'
app.register_blueprint(bp, url_prefix=PREFIX)
app.register_blueprint(api, url_prefix=PREFIX+'/api')
app.register_blueprint(auth, url_prefix=PREFIX+'/auth')
app.register_blueprint(posts, url_prefix=PREFIX+'/posts')
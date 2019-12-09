import flask
import pymongo
class MongoDBDAO:
  def __init__(self, hostname):
    self.db = pymongo.MongoClient('mongodb://root:root@'+hostname).db

  def get_username(self, sid):
    try:
      result = self.db.session.find_one({'sid':sid})
      username = result.get('username') if result else None
      return username
    except Exception as err:
      flask.flash(f"Database error: {err}")
      return None

  def get_password(self, username):
    try:
      result = self.db.user.find_one({'username':username})
      password = result.get('password') if result else None
      return password
    except Exception as err:
      flask.flash(f"Database error: {err}")
      return None

  def set_session(self, sid, username):
    try:
      self.db.session.insert({'sid':sid, 'username':username})
    except Exception as err:
      flask.flash(f"Database error: {err}")

  def add_post(self, username, post):
    try:
      self.db.posts.insert({'username':username, 'post':post})
    except Exception as err:
      flask.flash(f"Database error: {err}")

  def get_posts(self, username):
    try:
      posts = self.db.posts.find({'username':username})
      if posts == None:
        return ["(nie masz postów)"]
      return [p.get('post') for p in posts]
    except Exception as err:
      flask.flash(f"Database error: {err}")
      return []

  def get_post(self, username, index):
    try:
      result = self.db.posts.find_one({'username':username, 'id':index})
      post = result.get('post') if result else None
      return post
    except Exception as err:
      flask.flash(f"Database error: {err}")
      return None

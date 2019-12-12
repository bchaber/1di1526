import time
import flask
import pymongo

DESC = pymongo.DESCENDING
class MongoDBDAO:
  def __init__(self, hostname):
    db = None
    while db is None:
      try:
        db = pymongo.MongoClient('mongodb://root:root@'+hostname).db
      except Exception as err:
        print(f"Error while connecting with MongoDB: {err}")
      time.sleep(1)
    print("Connected to MongoDB")
    self.db = db

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
      counter = self.db.counters.find_and_modify({'name':'posts'}, 
        {'$inc':{'value':1}}, new=True)
      index = counter.get('value')
      self.db.posts.insert({'username':username, 'post':post, 'id':index})
      print(f"Post id: {index}")
    except Exception as err:
      flask.flash(f"Database error: {err}")

  def get_posts(self, username):
    try:
      posts = self.db.posts.find({'username':username}).sort('id',DESC).limit(4)
      if posts.count() == 0:
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

import time
import flask
import pymongo

DESC = pymongo.DESCENDING
class MongoDBDAO:
  def connect(self, hostname, username, password):
    try:
      db = pymongo.MongoClient(f'mongodb://{username}:{password}@{hostname}').db
      return db
    except Exception as err:
      print(f"Error while connecting with MongoDB: {err}")
      time.sleep(1)
      return None
  
  def test_database(self):
    try:
      return self.db.user.find({}).count()
    except Exception as err:
      print(f"Error while testing collections: {err}")
      time.sleep(1)
      return None

  def __init__(self, hostname):
    self.db = None
    while self.db is None:
      self.db = self.connect(hostname, "root", "root")
    if not self.test_database():
      print(f"Initiating collections")
      import app.init_mongodb
    print("Connected to MongoDB")
    
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

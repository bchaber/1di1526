import random
import string
from redis import Redis
from flask import Flask
from flask import request
from flask import make_response

class RedisDAO:
  def __init__(self, db):
    self.db = db
  def get_username(self, sid):
    username = self.db.hget("session:" + sid, "username")
    return username
  def get_password(self, username):
    password = self.db.get("user:" + username)
    return password
  def set_session(self, sid, username):
    self.db.hset("session:" + sid, "username", username)
  def add_post(self, username, post):
    self.db.lpush("posts:" + username, post)
  def get_posts(self, username):
    posts = self.db.lrange("posts:" + username, 0, 3)
    if len(posts) == 0:
      return ["(nie masz postów)"]
    return posts
  def get_post(self, username, index):
    post = self.db.lindex("posts:" + username, index)
    return post

app = Flask(__name__)
db = Redis("db", decode_responses=True, charset="utf-8")
dao = RedisDAO(db)
    
@app.route('/login')
def login():
  return """<!doctype html>
<head/>

<form action="/auth" method="POST">
 <input type="text" name="username"></input>
 <input type="password" name="password"></input>
 <input type="submit"/>
</form>
"""

@app.route('/')
def index():
  session_id = request.cookies.get('session_id','')
  print(f"/ session {session_id}")
  response = make_response('', 303)
  username = dao.get_username(session_id)
  if username:
    response.headers["Location"] = "/welcome"
  else:
    response.headers["Location"] = "/login"
  return response

@app.route('/welcome')
def welcome():
  session_id = request.cookies.get('session_id','')
  print(f"/welcome session {session_id}")
  username = dao.get_username(session_id)
  if username:
    posts = dao.get_posts(username)
    posts = '</li><li>'.join(posts)
    return f"""<!doctype html>
<head/>

Witaj {username}!
Wiadomości: <ul><li>{posts}</li></ul>
Ustaw wiadomość:
<form action='/post' method='post'>
<input type='text' name='post'/>
<input type='submit'/>
</form>
""", 200
  else:
    response = make_response('', 303)
    response.set_cookie("session_id", "", max_age=-1)
    response.headers["Location"] = "/login"
    print(f"/welcome removing session {session_id}")
    return response

@app.route('/auth', methods=['POST'])
def auth():
  username = request.form.get('username')
  password = request.form.get('password')
  if password != dao.get_password(username):
    return "Niepoprawna nazwa użytkownika lub hasło", 403

  session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
  dao.set_session(session_id, username)
  print(f"New session {session_id} for {username}")
  response = make_response('', 303)
  response.set_cookie("session_id", session_id, max_age=1800)
  response.headers["Location"] = "/"

  return response

@app.route('/post', methods=['POST'])
def new_post():
  response = make_response('', 303)
  session_id = request.cookies.get('session_id','')
  print(f"/post session {session_id}")
  username = dao.get_username(session_id)
  if username:
    post = request.form.get('post')
    dao.add_post(username, post)
    print(f'/post added new post for {username}/{session_id}')
    response.headers["Location"] = "/welcome"
  else:
    response.headers["Location"] = "/login"
  return response

@app.route('/post/<username>/<post>', methods=['GET'])
def get_post(username, post):
  post = dao.get_post(username, post)
  return post or 'Nothing', 404

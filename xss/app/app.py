import os
import random
import string
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from .redis_dao import RedisDAO
from .mariadb_dao import MariaDBDAO
from .mongodb_dao import MongoDBDAO

from time import sleep
print("Waiting 10s for DB to start...")
sleep(10)
print("...done")

app = Flask(__name__)
DB = os.getenv("DB")
print(f"DB is {DB}")
if DB == "MongoDB":
  dao = MongoDBDAO("db")
if DB == "MariaDB":
  dao = MariaDBDAO("db")
if DB == "Redis":
  dao = RedisDAO("db")
app.secret_key = 'deadbeef'
   
@app.route('/login')
def login():
  return render_template("index.html", content="""
<form action="/auth" method="POST">
 <input type="text" name="username"></input>
 <input type="password" name="password"></input>
 <input type="submit"/>
</form>
""")

@app.route('/')
def index():
  session_id = request.cookies.get('session_id','')
  print(f"/ session {session_id}")
  response = make_response('', 303)
  username = dao.get_username(session_id)
  print(f"/ username for {session_id} is {username}")
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
    return render_template("index.html", content=f"""
Witaj {username}!
Wiadomości: <ul><li>{posts}</li></ul>
Ustaw wiadomość:
<form action='/post' method='post'>
<input type='text' name='post'/>
<input type='submit'/>
</form>
"""), 200
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
  print(f"/auth {username}: {password}")
  if password != dao.get_password(username):
    return render_template("index.html", content=f"Niepoprawna nazwa użytkownika lub hasło"), 403

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
    print(f"/post added new post for {username}/{session_id}")
    response.headers["Location"] = "/welcome"
  else:
    response.headers["Location"] = "/login"
  return response

@app.route('/api/post', methods=['GET'])
def get_post():
  body = request.get_json()
  if body is None:
    return "Nothing", 400
  post = dao.get_post(body.get('username'), body.get('index'))
  if post is None:
    return "Nothing", 404
  return post

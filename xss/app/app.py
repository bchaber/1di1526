from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from .dao import dao
from .app_auth import app_auth
from .app_api import app_api
from .app_posts import app_posts

from time import sleep
print("Waiting 10s for DB to start...")
sleep(10)
print("...done")

app = Flask(__name__)
app.secret_key = 'deadbeef'
app.register_blueprint(app_auth)
app.register_blueprint(app_api)
app.register_blueprint(app_posts)

@app.route('/')
def index():
  session_id = request.cookies.get('session_id','')
  response = make_response('', 303)
  username = dao.get_username(session_id)
  print(f"/ username for {session_id} is {username}")
  response.headers["Location"] = "/welcome" if username else "/login"
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
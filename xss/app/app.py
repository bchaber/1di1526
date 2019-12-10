from flask import Flask
from flask import request, url_for
from flask import make_response
from flask import render_template
from .dao import dao
from .api import api
from .auth import auth
from .posts import posts

from time import sleep
print("Waiting 10s for DB to start...")
sleep(10)
print("...done")

app = Flask(__name__)
app.secret_key = 'deadbeef'
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(posts, url_prefix='/posts')

@app.route('/')
def index():
  session_id = request.cookies.get('session_id','')
  response = make_response('', 303)
  username = dao.get_username(session_id)
  print(f"/ username for {session_id} is {username}")
  response.headers["Location"] = \
    url_for("welcome" if username else "auth.login")
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
<form action='/posts/' method='post'>
<input type='text' name='post'/>
<input type='submit'/>
</form>
"""), 200
  else:
    response = make_response('', 303)
    response.set_cookie("session_id", "", max_age=-1)
    response.headers["Location"] = url_for("auth.login")
    print(f"/welcome removing session {session_id}")
    return response
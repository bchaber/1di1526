import random
import string
from flask import Blueprint
from flask import request, make_response, render_template, url_for
from .dao import dao

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
  auth_url = url_for(".authorize")
  return render_template("index.html", content=f"""
<form action="{auth_url}" method="POST">
 <input type="text" name="username" placeholder="username"></input>
 <input type="password" name="password" placeholder="password"></input>
 <input type="submit"/>
</form>
""")

@auth.route('/', methods=['POST'])
def authorize():
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
  response.headers["Location"] = url_for("bp.index")

  return response

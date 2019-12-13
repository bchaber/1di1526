from flask import Blueprint
from flask import request, url_for
from flask import make_response
from flask import render_template
from .dao import dao

bp = Blueprint('bp', __name__, template_folder='templates')

@bp.route('/')
def index():
  session_id = request.cookies.get('session_id','')
  response = make_response('', 303)
  username = dao.get_username(session_id)
  print(f"/ username for {session_id} is {username}")
  response.headers["Location"] = \
    url_for(".welcome" if username else "auth.login")
  return response

@bp.route('/welcome')
def welcome():
  new_post_url = url_for("posts.new_post")
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
<form action='{new_post_url}' method='post'>
<input type='text' name='post' placeholder='text to be posted'/>
<input type='submit'/>
</form>
"""), 200
  else:
    response = make_response('', 303)
    response.set_cookie("session_id", "", max_age=-1)
    response.headers["Location"] = url_for("auth.login")
    print(f"/welcome removing session {session_id}")
    return response
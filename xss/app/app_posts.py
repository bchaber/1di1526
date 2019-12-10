from flask import Blueprint, make_response, request, render_template
from .dao import dao

app_posts = Blueprint('app_posts', __name__, template_folder='templates')

@app_posts.route('/post', methods=['POST'])
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
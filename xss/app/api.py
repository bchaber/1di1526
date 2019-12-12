from flask import Blueprint, request
from .dao import dao

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/post', methods=['GET'])
def get_post():
  body = request.get_json()
  if body is None:
    body = request.args.copy()
    index = body.get('index','')
    try:
      index = int(index)
    except ValueError:
      print(f"/api/post Couldn't cast the index value '{index}' to int")
      index = -1
    body['index'] = index
  print(f"/api/post {body}")
  password = dao.get_password(body.get('username'))
  if password != body.get('password'):
    return "Forbidden", 403
  post = dao.get_post(body.get('username'), body.get('index'))
  if post is None:
    return "Nothing", 404
  return post

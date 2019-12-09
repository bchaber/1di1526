from redis import Redis
class RedisDAO:
  def __init__(self, hostname):
    self.db = Redis(hostname, decode_responses=True, charset="utf-8")

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
import pymongo
db = pymongo.MongoClient("mongodb://root:root@mongodb").db
db.counters.remove({})
db.counters.insert({"name":"posts","value":0})
db.user.remove({})
db.user.insert({'username':'bach', 'password':'haslo'})
db.user.insert({'username':'john', 'password':'snow'})
db.user.insert({'username':'bob',  'password':'bob'})
db.session.remove({})
db.session.insert({'sid':'deadbeef', 'username':'bach'})
db.posts.remove({})

for u in db.user.find():
  print(u)

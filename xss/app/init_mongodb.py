import pymongo
db = pymongo.MongoClient("mongodb://root:root@db").db
db.user.remove({})
db.user.insert({'username':'bach', 'password':'haslo'})
db.user.insert({'username':'john', 'password':'snow'})
db.user.insert({'username':'bob',  'password':'bob'})
db.session.remove({})
db.session.insert({'sid':'deadbeef', 'username':'bach'})
db.posts.remove({})
db.posts.insert({'username':'bach','post':'Hello!','id':1})

for u in db.user.find():
  print(u)

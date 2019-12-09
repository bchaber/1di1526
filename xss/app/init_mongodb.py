import pymongo
db = pymongo.MongoClient("mongodb://root:root@db").db
db.user.delete({})
db.user.insert({'username':'bach', 'password':'haslo'})
db.user.insert({'username':'john', 'password':'snow'})
db.user.insert({'username':'bob',  'password':'bob'})
db.session.delete({})
db.session.insert({'sid':'deadbeef', 'username':'bach'})
db.posts.delete({})
db.posts.insert({'username':'bach','post':'Hello!'})

for u in db.user.find():
  print(u)

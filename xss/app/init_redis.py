from redis import Redis
db = Redis("redis")
db.flushall()
db.set("user:bach", "haslo")
db.set("user:john", "snow")
db.set("user:bob",  "bob")

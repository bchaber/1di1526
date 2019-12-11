from redis import Redis
db = Redis("redis")
db.set("user:bach", "haslo")
db.set("user:john", "snow")
db.set("user:bob",  "bob")

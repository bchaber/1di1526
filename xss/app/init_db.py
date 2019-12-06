from redis import Redis
db = Redis("db")
db.set("user:bach", "haslo")
db.set("user:john", "snow")
db.set("user:bob",  "bob")

from redis import Redis
db = Redis("redis")
db.flushall()
db.set("user:bach", "haslo")
db.set("user:john", "snow")
db.set("user:bob",  "bob")
for i in range(1,30):
    db.set(f"user:user{i}", "pass")
db.lpush("posts:bob" , "To jest sekret!")

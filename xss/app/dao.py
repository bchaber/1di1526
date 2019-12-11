import os
from .redis_dao import RedisDAO
from .mariadb_dao import MariaDBDAO
from .mongodb_dao import MongoDBDAO

DB = os.getenv("DB")
if DB not in ("mongodb", "mariadb", "redis"):
    print(f"Unsupported DAO type: {DB}")
print("== Creating DAO")
if DB == "mongodb":
  dao = MongoDBDAO(DB)
if DB == "mariadb":
  dao = MariaDBDAO(DB)
if DB == "redis":
  dao = RedisDAO(DB)

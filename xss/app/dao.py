import os
from .redis_dao import RedisDAO
from .mariadb_dao import MariaDBDAO
from .mongodb_dao import MongoDBDAO

DB = os.getenv("DB")
if DB not in ("MongoDB", "MariaDB", "Redis"):
    print(f"Unsupported DAO type: {DB}")
print("== Creating DAO")
if DB == "MongoDB":
  dao = MongoDBDAO("db")
if DB == "MariaDB":
  dao = MariaDBDAO("db")
if DB == "Redis":
  dao = RedisDAO("db")
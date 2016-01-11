#===============================================================================
# @author roger
#===============================================================================
from pymongo import MongoClient
from conf import cfg

def get_db():
    print cfg.getProperty("database", "DB_HOST");
    client = MongoClient(cfg.getProperty("database", "DB_HOST"), int(cfg.getProperty("database", "DB_PORT")))
    db = client[cfg.getProperty("database", "DB_NAME")]
    return db

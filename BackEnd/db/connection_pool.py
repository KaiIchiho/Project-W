import mariadb
from config import setting_database

pool=None

def init_pool():
    global pool
    pool=mariadb.ConnectionPool(
        pool_name="db_connection_pool",
        pool_size=5,
        user=setting_database.USER,
        password=setting_database.PASSWORD,
        host=setting_database.HOST,
        port=setting_database.PORT,
        database=setting_database.DATABASE
    )
    
def get_connection():
    global pool
    if pool is None:
        return None
    try:
        return pool.get_connection()
    except Exception as e:
        print("Error: DB Connection error: ", e)
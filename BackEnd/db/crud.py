from db import connection_pool
from contextlib import contextmanager
from config import setting_database

def read_data(sql:str,params=None):
    try:
        with _get_db() as conn:
            cur=conn.cursor(dictionary=True)
            cur.execute(sql,params)
            return cur.fetchall()
    except Exception as e:
        print("Error, DB Error: ",e)
        return None

def insert_data(sql:str,params=None)->bool:
    try:
        with _get_db() as conn:
            cur=conn.cursor()
            cur.execute(sql,params)
            conn.commit()
            # return cur.lastrowid()
            return True
    except Exception as e:
        print("Error, DB Error: ",e)
        return False

@contextmanager
def _get_db():
    conn=connection_pool.get_connection()
    try:
        yield conn
    finally:
        if conn:
            conn.close()

def _check_bool(result)->bool:
    if result:
        return True
    else:
        return False

def _check_table_name(table:str)->bool:
    if table in setting_database.ALLOWED_TABLES:
        return True
    else:
        return False

def read_all_data_by_table(table:str)->list[dict]:
    if not _check_table_name(table):
        raise ValueError(f"Invalid table: {table}")
    
    sql=f"SELECT * FROM {table}"
    return read_data(sql)

def check_is_id_exist_by_table(table:str,id)->bool:
    if not _check_table_name(table):
        raise ValueError(f"Invalid table: {table}")
    
    sql=f"SELECT 1 FROM {table} WHERE id = ?"
    result=read_data(sql,(id,))
    return _check_bool(result)
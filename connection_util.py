import sqlite3


def create_connection(db_file: str):
    try:
        return sqlite3.connect(db_file)
    except Exception as e:
        print(e)


def close_connection(conn):
    try:
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

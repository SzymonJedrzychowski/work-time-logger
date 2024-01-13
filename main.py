import psutil
import win32gui
import win32process
import sqlite3
import time

NAMES_MAP = {}


def main():
    conn = create_connection("data/logs.db")

    cur = conn.cursor()

    sql = "SELECT * FROM names"
    cur.execute(sql)

    results = cur.fetchall()

    for res in results:
        NAMES_MAP[res[1]] = res[0]

    while True:
        time.sleep(30)
        if is_screen_locked():
            write_data(conn, None)
        else:
            name = active_window_process_name()
            write_data(conn, name)


def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()
    except:
        pass


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


def is_screen_locked():
    for proc in psutil.process_iter():
        if proc.name() == "LogonUI.exe":
            return True
    return False


def write_data(conn, name):
    global NAMES_MAP

    if name is not None:
        if name in NAMES_MAP:
            name = NAMES_MAP[name]
        else:
            sql = "INSERT INTO names(process_name) VALUES(?)"
            data = (name,)
            curr = conn.cursor()
            curr.execute(sql, data)

            NAMES_MAP[name] = curr.lastrowid
            name = curr.lastrowid

    sql = "INSERT INTO logs(name, time) VALUES(?, ?)"
    data = (name, int(time.time()))

    curr = conn.cursor()
    curr.execute(sql, data)
    conn.commit()


if __name__ == '__main__':
    main()

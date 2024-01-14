import psutil
import win32gui
import win32process
from connection_util import create_connection, close_connection
import time

NAMES_MAP = {}


def load_data():
    conn = create_connection("data/logs.db")

    cur = conn.cursor()

    sql = "SELECT * FROM names"
    cur.execute(sql)

    results = cur.fetchall()

    for res in results:
        NAMES_MAP[res[1]] = res[0]

    close_connection(conn)


def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()
    except Exception as e:
        print(e)
        pass


def is_screen_locked():
    for proc in psutil.process_iter():
        if proc.name() == "LogonUI.exe":
            return True
    return False


def write_data(name):
    global NAMES_MAP

    conn = create_connection("data/logs.db")
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
    print(f"INSERTED: {data}")

    close_connection(conn)


def create_log():
    if is_screen_locked():
        write_data(None)
    else:
        name = active_window_process_name()
        write_data(name)

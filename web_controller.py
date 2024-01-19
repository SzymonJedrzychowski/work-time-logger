import time

from flask import render_template

from connection_util import create_connection, close_connection

DAY_LENGTH = 86000


def home(time_difference):
    conn = create_connection("data/logs.db")
    now = int(time.time())
    local_time = time.localtime()
    day_start = now - local_time.tm_hour * 3600 - local_time.tm_min * 60 - local_time.tm_sec

    week_start = day_start - local_time.tm_wday * 86400 + time_difference * 7 * DAY_LENGTH

    week_data = []
    for day in range(5):
        cur = conn.cursor()
        cur.execute(
            "SELECT logs.id, logs.time, names.process_name FROM logs LEFT JOIN names ON logs.name = names.id WHERE time >= ? AND time <= ?",
            (week_start + DAY_LENGTH * day, week_start + DAY_LENGTH * (day + 1)))
        data = cur.fetchall()
        week_data.append(data)
    close_connection(conn)
    week_data_len = [len(day_data) for day_data in week_data]
    return render_template("base.html", week_data=week_data, week_data_len=week_data_len, max_length=max(week_data_len),
                           render_time=render_time, calculate_nonsleep_time=calculate_nonsleep_time, sum=sum,
                           time_difference=time_difference)


def render_time(log_time):
    date = time.strftime("%H:%M", time.localtime(log_time))

    return date


def calculate_nonsleep_time(day_data):
    data = len(day_data) - [entry[2] for entry in day_data].count(None)
    return f"{data // 60}:{0 if data % 60 < 10 else ''}{data % 60}"

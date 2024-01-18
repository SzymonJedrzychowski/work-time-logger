import atexit
import time

from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from logging_util import create_log
from connection_util import create_connection, close_connection

DAY_LENGTH = 86000

app = Flask(__name__)


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=create_log, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def render_time(log_time):
    date = time.strftime("%H:%M", time.localtime(log_time))

    return date


def calculate_nonsleep_time(day_data):
    data = len(day_data) - day_data.count(None)
    return f"{data // 60}:{0 if data % 60 < 10 else ''}{data % 60}"


@app.route("/")
def home():
    conn = create_connection("data/logs.db")
    now = int(time.time())
    local_time = time.localtime()
    day_start = now - local_time.tm_hour * 3600 - local_time.tm_min * 60 - local_time.tm_sec

    week_start = day_start - local_time.tm_wday * 86400

    week_data = []
    for day in range(5):
        cur = conn.cursor()
        cur.execute(
            "SELECT logs.id, logs.time, names.process_name FROM logs JOIN names ON logs.name = names.id WHERE time >= ? AND time <= ?",
            (week_start + DAY_LENGTH * day, week_start + DAY_LENGTH * (day + 1)))
        data = cur.fetchall()
        week_data.append(data)
    close_connection(conn)
    week_data_len = [len(day_data) for day_data in week_data]
    return render_template("base.html", week_data=week_data, week_data_len=week_data_len, max_length=max(week_data_len),
                           render_time=render_time, calculate_nonsleep_time=calculate_nonsleep_time)


main()

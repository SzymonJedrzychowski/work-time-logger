import atexit
import time

from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler

import web_controller
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
    return web_controller.home(0)


@app.route("/<time_difference>")
def home_with_time(time_difference=0):
    print(time_difference)
    return web_controller.home(int(time_difference))


main()

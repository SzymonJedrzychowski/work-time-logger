import atexit

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from logging_util import create_log

app = Flask(__name__)


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=create_log, trigger="interval", seconds=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def home():
    return "Hello, world"


main()

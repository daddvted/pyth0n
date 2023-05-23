import time
from flask import Flask, request

app = Flask(__name__)


@app.route("/sleepy")
def sleepy():
    sec = int(request.args.get("sec", 2))
    time.sleep(sec)
    return f"done(sleep for {sec}s)"

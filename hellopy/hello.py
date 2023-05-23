import os
import socket

from flask import Flask
import redis
from redis import RedisError
from redis.sentinel import Sentinel, MasterNotFoundError

VERSION=1.0

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_pass = os.getenv("REDIS_PASS", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
name = os.getenv("WHO", "World")


app = Flask(__name__)


@app.route("/")
def hello():
    try:
        # sentinel = Sentinel([(redis_host, redis_port)], password=redis_pass)
        # r = sentinel.master_for('mymaster', socket_timeout=5)
        r= redis.Redis(host=redis_host, port=redis_port, db=0)
        visits = r.incr("counter")
    except (RedisError, MasterNotFoundError) as err:
        print(err)
        app.logger.info(str(err))
        visits = "<i>Cannot connect to Redis, counter disabled</i>"

    html = f"<h1 style='color: orangered;'>Hello {name}!</h1>" \
           "<p>Hostname:<b style='color: red;'> {hostname}</b></p>" \
           "<p>Visits: <b style='color: blue;'> {visits}</b></p>" \
           f"<p>Version: {VERSION}</p>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

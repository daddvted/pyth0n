from prometheus_client import start_http_server, Summary, Enum, Gauge
import random
import time

metric_values = [0, 1, 2]
status_values = [0, 1, 2, 3, 4]

coffee_maker_status = Gauge('coffee_maker_status', "Backup Status", ['status'])

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.

    while True:
        time.sleep(3)
        coffee_maker_status.labels(status=random.choice(status_values)).set(random.choice(metric_values))


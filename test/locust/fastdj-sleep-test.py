from locust import HttpUser, task


class FastDJTest(HttpUser):
    @task
    def sleep_test(self):
        self.client.get("/api/debug/sleep/10")
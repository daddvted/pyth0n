from locust import HttpLocust, TaskSet, task, between


class UserBehaviour(TaskSet):
    # def login(self):
    #     self.client.post("/login", {'username': 'ted', 'password': 'ted'})
    #
    # def logout(self):
    #     self.client.post("/logout", {'username': 'ted', 'password': 'ted'})

    # def on_start(self):
    #     self.login()
    #
    # def on_stop(self):
    #     self.logout()

    @task(1)
    def test_maillists(self):
        self.client.get('/api/maillists/')

    # @task(1)
    # def profile(self):
    #     self.client.get('/profile')


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)

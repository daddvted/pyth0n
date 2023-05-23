from locust import HttpLocust, TaskSet, task, between


class LDAPMAN_API_TESTER(TaskSet):
    token = ''
    headers = {}

    def on_start(self):
        self.login()

    def on_stop(self):
        print("stop tester")

    def login(self):
        r = self.client.post('/api/auth/login', {'username': 'ted', 'password': 'ted'})
        print(r.status_code)
        if r.status_code == 200:
            response_data = r.json()
            self.token = response_data['access_token']
            self.headers['Authorization'] = f'Bearer {self.token}'
        else:
            pass

    @task()
    def test_menu(self):
        self.client.get('/api/common/menu', headers=self.headers)

    @task()
    def test_users(self):
        self.client.get('/api/users/', headers=self.headers)

    @task()
    def test_groups(self):
        self.client.get('/api/groups/', headers=self.headers)

    @task()
    def test_maillist(self):
        self.client.get('/api/maillists/', headers=self.headers)

    @task()
    def get_api_maillist_all_group_member(l):
        l.client.get('/api/maillists/all_group/member', headers=l.headers)

    @task()
    def get_api_maillist_devops_group_member(l):
        l.client.get('/api/maillists/devops_group/member', headers=l.headers)


class APITester(HttpLocust):
    task_set = LDAPMAN_API_TESTER
    wait_time = between(2, 6)

import json
from urllib.parse import unquote_plus
from pygerrit2 import GerritRestAPI, HTTPBasicAuth



class GerritClient:
    def __init__(self):
        gerrit_url = 'http://10.0.0.111:8080'
        gerrit_username = 'admin'
        gerrit_password = 'bCgrphGpNjLc+bW9V03l20hU37YS3sMr5mZpMQaujA'

        auth = HTTPBasicAuth(gerrit_username, gerrit_password)
        self.client = GerritRestAPI(url=gerrit_url, auth=auth)

    
    def list_project(self):
        url = '/projects/'
        resp = self.client.get(url)
        return list(resp.keys())

    def list_project_access(self, project_name=None):
        if project_name:
            url = f'/projects/{unquote_plus(project_name)}/access'
            resp = self.client.get(url)
            print(json.dumps(resp, indent=2))
        else:
            all_accesses = []
            for project in self.list_project():
                url = f'/projects/{unquote_plus(project)}/access'
                resp = self.client.get(url)

                all_accesses.append(resp)

            print(json.dumps(all_accesses, indent=2))
    

    def list_group(self, simple=True):
        url = '/groups/'
        resp = self.client.get(url)
        all_groups = []
        for name, data in resp.items():
            group_id = data['id']
            member_url = f'{url}{group_id}/members'
            members = self.client.get(member_url)
            data['name'] = name
            if simple:
                data['members'] = [member['username'] for member in members]
            else:
                data['members'] = members
            
            all_groups.append(data)
        
        print(json.dumps(all_groups, indent=2))


    def debug(self):
        url = '/config/server/info'
        resp = self.client.get(url)
        print(json.dumps(resp, sort_keys=False, indent=4))




if __name__ == '__main__':
    gerrit = GerritClient()

    # print(gerrit.list_project())
    # gerrit.list_group()
    # gerrit.list_project_access('All-Projects')
    # gerrit.list_project_access('forbob')
    gerrit.debug()



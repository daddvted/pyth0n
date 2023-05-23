import re
import shutil
import requests
import tempfile
import pprint


class Nexus:
    def __init__(self):
        self.username = 'admin'
        self.password = 'zdsys8301'
        self.base_url = 'http://172.16.101.214:8081'

    def _fetch_url(self, url):
        response = requests.get(url, auth=(self.username, self.password))
        if not response.status_code == 200:
            print('Error getting {}'.format(url))
            return {}
        else:
            return response.json()

    def list_repos(self):
        repo_url = '{}/service/rest/v1/repositories'.format(self.base_url)
        return self._fetch_url(repo_url)

    def list_repo_components(self, repo_name, filter_regexp=r''):
        # Use 'filter_regexp' to filter component by name
        all_components = []
        components_url = '{}/service/rest/v1/components?repository={}'.format(self.base_url, repo_name)
        tmp = self._fetch_url(components_url)
        if tmp:
            all_components += tmp['items']
        else:
            return []

        while tmp['continuationToken']:
            new_url = '{}&continuationToken={}'.format(components_url, tmp['continuationToken'])
            tmp = self._fetch_url(new_url)
            all_components += tmp['items']

        if filter_regexp:

            filtered_components = list(filter(lambda x: re.match(filter_regexp, x['name']), all_components))
            return filtered_components

        else:
            return all_components

    def list_component(self, component_id):
        component_url = '{}/service/rest/v1/components/{}'.format(self.base_url, component_id)
        return self._fetch_url(component_url)

    def delete_component(self, component_id):
        component_url = '{}/service/rest/v1/components/{}'.format(self.base_url, component_id)
        response = requests.delete(component_url, auth=(self.username, self.password))
        if response.status_code == 204:
            print('Delete component({}) successfully'.format(component_id))
        else:
            print('Delete component({}) unsuccessfully'.format(component_id))

    # To be optimized
    def transfer_maven_componemt(self):
        # print(type(tmp_jar))

        source = 'maven-hosted'
        # components = self.list_repo_components(source)
        components = self.list_repo_components(source, r'rate')
        for comp in components:
            # jar = tempfile.TemporaryFile()
            # jar = tempfile.mkstemp()
            source_url = comp['assets'][0]['downloadUrl']
            # open(tmp_jar, 'rb') as jar:

            # with tempfile.TemporaryFile() as jar:
            with requests.get(source_url, stream=True) as r,\
                open('tmp.jar', 'wb') as jar:
                # print(r.content)
                shutil.copyfileobj(r.raw, jar)

            with open('tmp.jar', 'rb') as jar:
               form_data = {
                   'maven2.groupId': (None, comp['group']),
                   'maven2.artifactId': (None, comp['name']),
                   'maven2.version': (None, comp['version']),
                   'maven2.generate-pom': (None, 'false'),
                   'maven2.asset1': jar.read(),
                   'maven2.asset1.extension': (None, 'jar')
               }
               print('Transfering: {}.{}.{}'.format(comp['group'], comp['name'], comp['version']))

               # Disable Self-signed TLS error
               import urllib3
               urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
               r = requests.post('https://nexus.ted.mighty/service/rest/v1/components?repository=m2-hosted',
                                 verify=False, auth=('user', 'user'), files=form_data)
               if r.status_code == 204:
                   print("success")


if __name__ == '__main__':
    nexus = Nexus()
    nexus.transfer_maven_componemt()

    # components = nexus.list_components('zdsys', filter_regexp=r'.+\-building')
    # for component in components:
    #    print(component['id'])
    #    delete_component(component['id'])
    #    time.sleep(2)

    # foo = nexus.list_component(cid)
    # print(foo)
    # url = 'http://172.16.101.214:8081/repository/maven-hosted/com/wish30/1.6/wish30-1.6.jar'
    # local_filename = url.split('/')[-1]
    #
    #

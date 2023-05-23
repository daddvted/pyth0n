from jira import JIRA


jira = JIRA(server='http://172.16.101.172',auth=('zhangpeng', 'wh@theFuck'))

for proj in jira.projects():
    print(proj)

from jira.client import GreenHopper
options = {'server': 'http://172.16.101.172'}
gh = GreenHopper(options, basic_auth=('zhangpeng', 'wh@theFuck'))

print(gh.boards())
for board in gh.boards():
    print(board.name)
    print(board.id)
    print('---------------------------------')
    print(jira.sprints(board.id))


print(jira.sprint_info(69, 85))

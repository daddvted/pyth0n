import time
import codecs
import requests
import lxml.html


# http://infomap.cdedu.com/Home/Index?all=1&per=b4152536-3c7d-46a6-9738-93e237d985ce&pages=1
# 学校学段：小学
# 办学性质：不限
# 所在区域：不限

class CDSchool:

    def __init__(self):
        self.url_tpl = 'http://infomap.cdedu.com/Home/Index?all=1&per=b4152536-3c7d-46a6-9738-93e237d985ce&pages={}'

    def get_total_page(self, xpath):
        url = self.url_tpl.format(1)
        resp = requests.get(url)
        if resp.status_code == 200:
            html = lxml.html.fromstring(resp.text)
            page_element = html.xpath(xpath)
            page = page_element[0].text_content()
            return int(page)
        else:
            print('获取页面失败')
            return -1

    def crawl(self, xpath, total_page, filename, sleep=2):

        for p in range(1, total_page + 1):
            # print(f"crawling on page: {p}")
            response = requests.get(self.url_tpl.format(p))
            if response.status_code == 200:
                print('success on page: {}'.format(p))
                html = lxml.html.fromstring(response.text)
                lis = html.xpath(xpath)
                self._parse(filename, lis)
            else:
                print('failed on page: {}'.format(p))

            time.sleep(sleep)

    @staticmethod
    def _parse(filename, elements):
        with codecs.open(filename, mode='a', encoding='utf-8') as out:
            for element in elements:
                print(str(element.text_content()),file=out)


if __name__ == '__main__':
    cdschool = CDSchool()
    total = cdschool.get_total_page('/html/body/div[4]/div/div/p[7]')
    cdschool.crawl('/html/body/div[4]/ul/li', total_page=total, filename='eschool.txt')



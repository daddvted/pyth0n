import time
import requests
import lxml.html


url_template = 'https://movie.douban.com/top250?start={}&filter='

with open('movies.txt', 'w') as f:
    for page in range(0, 10):
        print("抓取第{}页".format(page + 1))

        url = url_template.format(page * 25)
        http_response = requests.get(url)
        http_response.encoding = "utf-8"
        html = lxml.html.fromstring(http_response.text)
        movies = html.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for movie in movies:
            text = str(movie.text_content())

            # 可以使用print来输出文本看下是什么样子
            # print(text)

            # 也可以通过repr()方法来显示字符串里的特殊字符
            #print(repr(text))

            # 稍微处理一下，替换掉字符串中的特殊字符'\n'
            clean_text = text.replace('\n', '')
            print(clean_text, file=f)

        # 抓取数据的时候稍等停顿一下，不要对目标网站造成太大的压力
        time.sleep(3)

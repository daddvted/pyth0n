import requests
import lxml.html

# 获取豆瓣电影Top250的网页
http_response = requests.get("https://movie.douban.com/top250")
# 根据网页的charset来设置对应的中文编码
http_response.encoding = "utf-8"

# 将HTTP响应的HTML文本通过lxml.html.fromstring方法
# 转换成可以使用XPath的来分析的对象
html = lxml.html.fromstring(http_response.text)

# 通过谷歌浏览器的开发者工具获取电影列表的<li>元素
movies = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

for movie in movies:
    # 获取第一个电影标题所在的元素
    first_title_element = movie.xpath('.//span[@class="title"][1]')

    # 使用XPath的text_content()方法来获取元素的文本
    title = first_title_element[0].text_content()

    # 获取电影评分所在的元素
    rating_element = movie.xpath('.//span[@class="rating_num"]')

    # 使用同样的方式来获取文本
    rating = rating_element[0].text_content()

    # 格式化输出电影标题及评分
    print('<<{}>> - {}'.format(title, rating))

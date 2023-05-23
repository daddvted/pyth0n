import requests
import lxml.html

with open('books.txt', 'w', encoding='utf-8') as f:
    for page in range(1, 10):
        # 使用Python的for循环语句跟format格式化字符串方法来自动生成书籍的分页URL
        url = 'http://yuedu.163.com/book/category/category/2100/0_0_1/p{}/s20'.format(page)

        # 获取网易云阅读文字作品网页
        http_response = requests.get(url)
        # 设置中文编码
        http_response.encoding = "utf-8"

        html = lxml.html.fromstring(http_response.text)

        # 通过谷歌开发者工具来辅助获取书籍列表的<div>元素
        books = html.xpath('//*[@id="page-163-com"]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/div')
        
        # 输出一些信息，便于显示抓取进度
        print("====== 第{}页, 书籍{}本 ======".format(page, len(books)))
        for book in books:
            # 获取标题
            title = book.xpath('.//h2')[0].text_content()
            # 获取作者
            author = book.xpath('.//dd')[0].text_content()
            # 获取评分
            spans = book.xpath('.//span[@class="no"]')
            rate = 5 - len(spans)

            # 将书名，作者，评分通过逗号连接起来，作为一行保存到文件里
            print('{},{},{}'.format(title, author, rate), file=f)
        
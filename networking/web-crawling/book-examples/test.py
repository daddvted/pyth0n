import lxml.html


with open("4-1.html", "r", encoding="utf-8") as f:
    a = f.read()


html = lxml.html.fromstring(a)

r = html.xpath('//td[@class="history  "]')
print(r)
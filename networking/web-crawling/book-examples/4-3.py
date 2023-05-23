import lxml.html

with open('4-2.html', 'r', encoding='utf-8') as f:
    # 通过lxml.html.fromstring()方法
    # 将保存在4-2.html中的HTML代码转换成HTML对象
    html = lxml.html.fromstring(f.read())

print('HTML对象: {}')
print(html)

# ====== 选择所有的<div>元素 ======
all_div = html.xpath('//div')
print('\n所有的<div>元素(2个): ')
# all_div是一个列表，里面保存了2个<div>元素
print(all_div)

# ====== 选择“水果列表”的<div>元素 ======
fruit_div = html.xpath('//div[@class="fruit"]')
print('\n“水果列表”的<div>元素: ')
print(fruit_div)

# ====== 选择所有的<li>元素 ======
all_li = html.xpath('//li')
print('\n所有的<li>元素: ')
print(all_li)

# ====== 先选择“水果列表”<div>，再选择下面的<li> ======

# 由于xpath()方法会返回一个列表，而且这个列表只有一个元素，
# 所以使用序号0来选择列表中的元素
fruit_div = html.xpath('//div[@class="fruit"]')[0]

# XPath使用"."表示从当前<div>开始选择
fruit_li = fruit_div.xpath('.//li')

# XPath不使用"."
wrong_fruit_li = fruit_div.xpath('//li')

print('\n使用了"."的选择结果: ')
print(fruit_li)
print('未使用"."的选择结果: ')
print(wrong_fruit_li)

# ======= 选择“苹果”元素 ======
apple_li = html.xpath('//li[@id="apple"]')
print('\n“苹果”元素: ')
print(apple_li)

# ======= 选择第一个<div>元素 =======
first_div = html.xpath('//div[1]')
print('\n第1个<div>: ')
print(first_div)

# ======= 选择所有带有class="special"的元素 =======
special_li = html.xpath('//*[@class="special"]')
print('\n带有class="special"的元素: ')
print(special_li)
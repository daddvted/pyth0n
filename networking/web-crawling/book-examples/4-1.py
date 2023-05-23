import requests
import lxml.html

# 获取中国天气网天气预报网页
http_response = requests.get("http://www.weather.com.cn/weather1d/101270101.shtml")
# 设置中文编码
http_response.encoding = "utf-8"

html = lxml.html.fromstring(http_response.text)

# 获取白天温度数据所在的HTML元素(这里是叫span的元素)
day_temperature_span = html.xpath('//*[@id="today"]/div[2]/ul/li[1]/p[2]/span')
# 获取夜间温度数据所有的HTML元素
night_temperature_span =  html.xpath('//*[@id="today"]/div[2]/ul/li[2]/p[2]/span')

# 获取白天温度数据
day_temperature = day_temperature_span[0].text_content()
# 获取夜间温度数据
night_temperature = night_temperature_span[0].text_content()

# 将温度数据格式化之后打印输出
print('{}°C ~ {}°C'.format(day_temperature, night_temperature))
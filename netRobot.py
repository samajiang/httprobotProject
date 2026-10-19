import requests
from lxml import html

#定义url访问网站
url = 'https://www.tiobe.com/tiobe-index/'
#定义headers
headers = {
    'User-Agent': 'jibarobot'
}
#发送请求
response = requests.get(url, headers=headers)
# #打印状态码
# print(response.status_code)
# #打印响应内容
# print(response.text)

#解析html文件
document = html.fromstring(response.text)

#使用xpath拿取想要的数据
needdate = document.xpath("//table[@id='top20']/thead/tr/th/text()")
print(needdate)
datenumble = document.xpath("//table[@id='top20']/tbody/tr")
for i in datenumble:
    turledate = i.xpath("./td/text()")
    print(turledate)




import requests

#定义url访问网站
url = 'https://www.tiobe.com/tiobe-index/'
#定义headers
headers = {
    'User-Agent': 'jibarobot'
}
#发送请求
response = requests.get(url, headers=headers)
#打印状态码
print(response.status_code)
#打印响应内容
print(response.text)

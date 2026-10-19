from lxml import html

# 读取html文件
with open("./resouce/test.html", encoding="UTF-8") as file:
    html_doc = file.read()

# 解析html文件，转换成一个文档对象
document = html.fromstring(html_doc)

#解析表头，xpath语法
headers = document.xpath("//div[@class='container main-content']/div/table/thead/tr/th/text()")
print(headers)
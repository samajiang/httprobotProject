import re
s1 = "18809090000是我的手机号，你记住了吗，我的另一个手机号是18800008888，两个qq号分别是155998992和18809091293821你记住了吗"
s2 = "我的手机号是18809090000，你记住了吗，我的另一个手机号是18800008888，两个qq号分别是155998992和18809091293821你记住了吗"

#match从字符串开头开始匹配
# result = re.match(r"1[3-9]\d{9}",s1)
# #获取字符串内容用group()
# print(result.group())
# #表示获取到的结果是从原字符串的什么位置到什么位置匹配的
# print(result.span())
# #表示从原字符串的哪个位置开始匹配上数据
# print(result.start())
# #表示从原字符串的哪个位置匹配上数据结束
# print(result.end())

#search从任意位置开始搜索第一个选项
# result = re.search(r"1[3-9]\d{9}",s2)
# print(result.group())
# print(result.span())
# print(result.start())
# print(result.end())

#findall搜索所有匹配项
result = re.findall(r"1[3-9]\d{9}",s2)
print(result)





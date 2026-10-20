#csv操作,文件操作的基本方式

#写
# with open("./resouce/csvtest.csv","w",encoding="utf-8")as f:
#     f.write("姓名,性别,年龄,爱好\n")#写入表头
#
#     f.write("ldd,nv,99,gogo\n")#写入数据(如果一格数据有逗号，需要用''括起来)
#     f.write("chen,nan,24,tietie")

#读取
# with open("./resouce/csvtest.csv","r",encoding="utf-8")as f:
#     for line in f:
#         print(line.strip())

#csv操作，使用标准csv库
import csv

#写
#     with open("./resouce/csvtest.csv","w",encoding="utf-8", newline="")as f:
#     #fieldnames表示表头
#     witer = csv.DictWriter(f, fieldnames=["name","sex","age","hobby"])
#     witer.writeheader()
#     witer.writerow({"name":"ldd","sex":"nv","age":99,"hobby":"gogo"})#写入数据

#读取
with open("./resouce/csvtest.csv","r",encoding="utf-8")as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

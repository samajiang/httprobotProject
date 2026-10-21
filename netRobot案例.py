import requests
import csv
from lxml import html

#定义常量
base_url = "https://www.themoviedb.org"
top_movie_url = "/movie/top-rated"
movie_list_file = "csv_date/movie_list.csv"

#获取电影详情函数
def get_movie_detail(mvurl):
    #1,发送请求,获取电影详情数据
    response = requests.get(mvurl,timeout=60)
    #2,解析数据，获取电影详情
    movie_doc = html.fromstring(response.text)
    #电影名称
    movie_name = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    #电影年份
    movie_year = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    #电影上映时间
    movie_release_date = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")
    #电影类型
    movie_type = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")
    #电影时长
    movie_duration = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")
    #电影评分
    movie_rating = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    #电影语言
    movie_language = movie_doc.xpath("// *[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    #3,返回电影详情-字典
    movieinfo = {
        "电影名称": movie_name[0].strip() if movie_name else '',
        "年份": movie_year[0].strip() if movie_year else '',
        "上映时间": movie_release_date[0].strip() if movie_release_date else '',
        "类型": ",".join(movie_type) if movie_type else '',
        "时长": movie_duration[0].strip() if movie_duration else '',
        "评分": movie_rating[0].strip() if movie_rating else '',
        "语言": movie_language[0].strip() if movie_language else ''
    }
    print(movieinfo)
    return movieinfo

#保存所有电影详情数据到csv文件的函数
def save_all_movies_info(all_movies_info):
    with open(movie_list_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["电影名称", "年份", "上映时间", "类型", "时长", "评分", "语言"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()#写入表头
        writer.writerows(all_movies_info)#写入数据


    pass

#主函数，定义核心逻辑
def main():
    #1,发送请求,获取高分电影榜单数据
    response = requests.get(base_url + top_movie_url,timeout=60)

    #2,解析数据，获取电影列表
    movie_doc = html.fromstring(response.text)
    movie_list = movie_doc.xpath("//div[@class='media-card-list contents w-full']/div/*")
    #3,遍历电影列表
    all_movies_info = []
    for movie in movie_list:
        movie_url = movie.xpath("./div[1]/div[2]/div[1]/a/@href")
        if movie_url:
            mvurl = base_url + movie_url[0]
            #获取电影详情
            movie_info = get_movie_detail(mvurl)
            all_movies_info.append(movie_info)
    #4,保存数据
    save_all_movies_info(all_movies_info)

if __name__ == '__main__':
    main()

import re

import requests
import csv
from lxml import html

#定义常量
base_url = "https://www.themoviedb.org"
top_movie_url1 = "/movie/top-rated"#默认访问第一页数据
top_movie_url2 = "/discover/movie/items"#访问第二页数据
movie_list_file = "csv_date/movie_list.csv"

#处理电影年份的函数
def get_year(movie_year):
    year = movie_year[0].strip() if movie_year else ''
    return year.replace('(','').replace(')','')

#处理电影上映时间的函数
def get_movie_release_date(movie_release_date):
    movie_date = movie_release_date[0].strip() if movie_release_date else ''#处理电影上映时间
    return  re.search(r"\d{4}-\d{2}-\d{2}", movie_date).group()

#处理电影时长的函数(统一转换为分钟)
def get_movie_duration(movie_duration):
    mduration = movie_duration[0].strip() if movie_duration else ''
    hours = re.search(r"(\d+)h", mduration)
    minutes = re.search(r"(\d+)m", mduration)
    h = int(hours.group(1)) if hours else 0#得到的结果是8h，所以用group(1)获取数字结果，不要h
    m = int(minutes.group(1)) if minutes else 0#得到的结果是8h，所以用group(1)获取数字结果，不要h
    totaltime = h * 60 + m
    return totaltime

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
    movie_release_date = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")
    #电影类型
    movie_type = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")
    #电影时长
    movie_duration = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")
    #电影评分
    movie_rating = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    #电影语言
    movie_language = movie_doc.xpath("// *[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    #3,返回电影详情-字典
    movieinfo = {
        "电影名称": movie_name[0].strip() if movie_name else '',
        "年份": get_year(movie_year),
        "上映时间": get_movie_release_date(movie_release_date),
        "类型": ",".join(movie_type) if movie_type else '',#因为类型可能有多个，所以用join连接，用逗号分隔
        "时长": get_movie_duration(movie_duration),
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
    #先定义一个空列表，用于存储所有电影详情数据
    all_movies_info = []
    #循环获取分页数据
    for num in range(1, 6):
        # 1,发送请求,获取高分电影榜单数据
        if num == 1:
            response = requests.get(base_url + top_movie_url1, timeout=60)
        else:
            # POST请求参数（修改页数，从第二页开始获取后边的数据）
            response = requests.post(base_url + top_movie_url2,
                                     "air_date.gte="
                                     "&air_date.lte="
                                     "&certification="
                                     "&certification_country=CN"
                                     "&debug="
                                     "&first_air_date.gte="
                                     "&first_air_date.lte="
                                     "&include_adult=false"
                                     "&include_softcore=false"
                                     "&latest_ceremony.gte="
                                     "&latest_ceremony.lte="
                                     f"&page={num}"
                                     "&primary_release_date.gte="
                                     "&primary_release_date.lte="
                                     "&region="
                                     "&release_date.gte="
                                     "&release_date.lte=2027-04-22"
                                     "&show_me=everything"
                                     "&sort_by=vote_average.desc"
                                     "&vote_average.gte=0"
                                     "&vote_average.lte=10"
                                     "&vote_count.gte=300"
                                     "&vote_count.lte="
                                     "&watch_region=CN"
                                     "&with_genres="
                                     "&with_keywords="
                                     "&with_networks="
                                     "&with_origin_country="
                                     "&with_original_language="
                                     "&with_watch_monetization_types="
                                     "&with_watch_providers="
                                     "&with_release_type="
                                     "&with_runtime.gte=0"
                                     "&with_runtime.lte=400"
                                     "&view="
                                     "&discover_preset=top-rated",
                                     timeout=60
                                     )

        # 2,解析数据，获取电影列表
        movie_doc = html.fromstring(response.text)
        movie_list = movie_doc.xpath("//div[@class='media-card-list contents w-full']/div/*")
        # 3,遍历电影列表
        for movie in movie_list:
            movie_url = movie.xpath("./div[1]/div[2]/div[1]/a/@href")
            if movie_url:
                mvurl = base_url + movie_url[0]
                # 获取电影详情
                movie_info = get_movie_detail(mvurl)
                all_movies_info.append(movie_info)

    #4,保存数据
    save_all_movies_info(all_movies_info)

if __name__ == '__main__':
    main()

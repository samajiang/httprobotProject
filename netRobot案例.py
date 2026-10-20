import requests
import csv
from lxml import html

#定义常量
base_url = "https://www.themoviedb.org"
top_movie_url = "/movie/top-rated"

#获取电影详情函数
def get_movie_detail(mvurl):
    pass

#保存所有电影详情数据到csv文件的函数
def save_all_movies_info(all_movies_info):
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

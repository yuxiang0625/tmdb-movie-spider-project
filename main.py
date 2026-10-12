# 导入爬虫所需的模块
import requests
import csv
from lxml import html

# 定义常量
MOVIE_LIST_CSV = './target_csv/movie_list.csv'
BASE_URL = 'https://www.themoviedb.org/'
URL = 'https://www.themoviedb.org/movie/top-rated'
URL_2 = 'https://www.themoviedb.org/discover/movie/items'
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

# 定义获取电影详情数据函数
def get_movie_info(movie_info_urls):
    movie_response = requests.get(movie_info_urls, headers=headers, timeout=60)
    movie_doc = html.fromstring(movie_response.text)
    movie_name = movie_doc.xpath('//head/meta[@property="og:title"]/@content')
    movie_year = movie_doc.xpath('//span[@class="release"]/text()')
    movie_type = movie_doc.xpath('//span[@class="genres"]/a/text()')
    movie_time = movie_doc.xpath('//span[@class="runtime"]/text()')
    movie_score = movie_doc.xpath('//div[@class="user_score_chart"]/@data-percent')
    movie_language = movie_doc.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    movie_director = movie_doc.xpath(
        '//li[contains(.,"Director")]/p[1]/a/text()'
    )
    movie_author = movie_doc.xpath(
        '//li[contains(.,"Writer") or contains(.,"Novel") or contains(.,"Story") or contains(.,"Screenplay")]/p[1]/a/text()'
    )
    movie_actor = movie_doc.xpath(
        '//*[@id="cast_scroller"]/ol/li/p[1]/a/text()'
    )
    movie_overview = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')
    #返回电影数据
    movie_data =  {
        '电影名': movie_name[0].strip() if movie_name else "",
        '年份': movie_year[0].strip() if movie_year else "",
        '类型': ','.join(movie_type) if movie_type else "",
        '时长': movie_time[0].strip() if movie_time else "",
        '评分': movie_score[0].strip() if movie_score else "",
        '语言': movie_language[0].strip() if movie_language else "",
        '导演': ','.join(movie_director) if movie_director else "",
        '编剧': ','.join(movie_author) if movie_author else "",
        '演员': ','.join(movie_actor) if movie_actor else "",
        '电影概述': movie_overview[0].strip() if movie_overview else ""
    }
    print(movie_data)  # 打印电影数据
    return movie_data

# 保存电影数据到csv文件
def save_movie_info_to_csv(all_movies):
    with open(MOVIE_LIST_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['电影名', '年份', '类型', '时长', '评分', '语言', '导演', '编剧', '演员', '电影概述'])
        writer.writeheader()
        writer.writerows(all_movies)
    print(f"数据已保存到 {MOVIE_LIST_CSV}")

# 定义主函数
def main():
    all_movie_info = []
    for page_num in range (1,6):
        if page_num == 1:
            # 发送HTTP请求获取网页内容
            response = requests.get(URL, timeout=60)
        else:
            response = requests.post(URL_2,
                                    data=f"air_date.gte=&air_date.lte=&certification=&certification_country=HK&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-12&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=HK&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated" ,
                                    timeout=60)
            # 解析网页内容，获取列表
        doc = html.fromstring(response.content)
        movie_list = doc.xpath(
                f'//*[@id="page_{page_num}"]/div/div/div[@class="w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300"]')
        # 遍历列表，获取所需数据

        for movie in movie_list:
            movie_urls = movie.xpath('./div/div/a/@href')
            movie_info_urls = BASE_URL + movie_urls[0]
            movie_info = get_movie_info(movie_info_urls)
            all_movie_info.append(movie_info)

    # 将数据保存到CSV文件中
    save_movie_info_to_csv(all_movie_info)

if __name__ == '__main__':
    main()


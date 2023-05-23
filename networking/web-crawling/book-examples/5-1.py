import re
import json

with open('movies.txt', 'r') as f, \
        open('data.json', 'w') as data :
    for line in f:
        # 替换多个空格为一个'#'号
        info = re.sub('\s{2,}', '#', line)

        info_list = info.split('#')
        # 获取电影排名
        ranking = info_list[1]
        # 获取电影标题
        title = info_list[2]

        # 获取电影国家
        match_countries = re.search('\d{4}.+\/(.+)\/', info)
        countries = match_countries.group(1).strip().replace(' ', ',')
        # print(countries)


        match_year = re.search('\d{4}', info)
        year = match_year.group(0)
        match_rating = re.search('\d\.\d', info)
        rating = match_rating.group(0)

        match_comment = re.search('(\d+)人评价', info)
        comment = match_comment.group(1)

        movie = {
            '排名': ranking,
            '名称': title,
            '国家': countries,
            '年份': year,
            '评分': rating,
            '评价人数': comment
        }

        s = json.dumps(movie)
        print(s, file=data)







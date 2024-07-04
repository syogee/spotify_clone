import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import re

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def pages(url):
# url = "https://isaiminiplay.com/movie-index?page=1"
    response = requests.get(url,verify=False)
    data = BeautifulSoup(response.content,"html.parser")
    no_of_pages = data.find('div',class_="total-pagination center-text")
    no_of_page = int(no_of_pages.get_text().strip().split(' ')[-1])
    return no_of_page

def movie_name(url,pages):
    movies = []
    for i in range(1,pages+1):
        url = url[:-1]+str(i)
        response = requests.get(url,verify=False)
        data = BeautifulSoup(response.content,"html.parser")
        movie = data.find_all('h2',class_='movie-name')
        for i in movie:
            movies.append(i.get_text())
    # print(movies)
    return movies

def url(movies):
    urls = []
    for m in movies:
        url = m.strip().replace(" ","-").lower()
        url = url.replace("-songs","").strip()
        re_space = re.sub(r'-+', '-', url)
        urls.append("-".join([re_space,"songs"]))
    return urls

if __name__=="__main__":
    all_movies_url = "https://isaiminiplay.com/movie-index?page=1"
    year_2024 = "https://isaiminiplay.com/tamil-songs-2024?page=1"
    year_2023 = "https://isaiminiplay.com/tamil-songs-2023?page=1"
    year_2022 = "https://isaiminiplay.com/tamil-songs-2022?page=1"
    year_2021 = "https://isaiminiplay.com/tamil-songs-2021?page=1"
    year_2020 = "https://isaiminiplay.com/tamil-songs-2020?page=1"
    year_2019 = "https://isaiminiplay.com/tamil-songs-2019?page=1"

    detail_all = pages(all_movies_url)
    detail_2024 = pages(year_2024)
    detail_2023 = pages(year_2023)
    detail_2022 = pages(year_2022)
    detail_2021 = pages(year_2021)
    detail_2020 = pages(year_2020)
    detail_2019 = pages(year_2019)
    print("Page details completed")

    all_movie = movie_name(all_movies_url,detail_all)
    movie_2024 = movie_name(year_2024,detail_2024)
    movie_2023 = movie_name(year_2023,detail_2023)
    movie_2022 = movie_name(year_2022,detail_2022)
    movie_2021 = movie_name(year_2021,detail_2021)
    movie_2020 = movie_name(year_2020,detail_2020)
    movie_2019 = movie_name(year_2019,detail_2019)
    print("Movie data completed")

    # movies=[]
    movies = all_movie + movie_2024 + movie_2023 + movie_2022 + movie_2021 + movie_2020
    # movies = all_movie + movie_2024
    sets = set(movies)
    lists = list(sets)
    dic = {}
    movie_urls = url(lists)
    dic["movie"]=movie_urls
    print(dic)
    print(len(movie_urls))
    data = pd.DataFrame(dic)
    data = data["movie"]
    data.to_excel("movie_url.xlsx",index=False)


import requests
from bs4 import BeautifulSoup as bs4
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://isaiminiplay.com/"

def movie_details(param):
    content = []
    for movie in param:
        # movie_name = movie.replace("-songs","").upper().replace("-"," ")
        details = {}
        urls = "".join([url,movie])
        response = requests.get(urls,verify=False)
        data = bs4(response.content,"html.parser")
        img = data.find("img")
        if img is not None:
            details[f"Image"] = "".join([url,img.get("src")[2:]])
        else :
            details[f"Image"] = "https://geo-media.beatsource.com/image_size/500x500/5/9/7/5974a942-7721-44db-982d-88b641bb4c94.jpg"


        movie_detail = data.find("fieldset",class_="album-info")
        if movie_detail is not None:
            strongs = movie_detail.find_all("strong")
            # span = movie_detail.find_all("span")
            for strong in strongs:
                key = strong.get_text().strip().rstrip(":")
                value = strong.find_next_sibling()
                if value is not None:
                    details[key]=value.text
        else:
            words = movie.replace("-songs","").replace("-"," ").split()
            capitalized_words = [word.capitalize() for word in words]
            details['Album'] = " ".join(capitalized_words)
        content.append(details)
    return content

def song_details(params):
    music_url = []
    i=0
    for movie in params:
        i+=1
        urls = "".join([url,movie])
        response = requests.get(urls,verify=False)
        data = bs4(response.content,"html.parser")
        songs = data.find_all("div", class_="song-deatils")
        for song in songs:
            songs_dic = {}
            strongs = song.find_all("strong")
            for strong in strongs:
                key = strong.get_text().strip().rstrip(":")
                value = strong.find_next_sibling()
                if value is not None:
                    songs_dic[key] = value.text.strip()
            song_name_url = song.find("button", class_="playbutton")
            onclick = song_name_url.get("onclick")
            start = onclick.find("'")+2
            end = onclick.find("'",start)
            songs_dic["Song URL"] = ("".join([url,onclick[start:end]]))
            song_name = song_name_url.get("data-title")
            songs_dic["Song Name"] = song_name
            movie_name = song_name_url.get("data-album")
            songs_dic["Album"] = movie_name
            music_url.append(songs_dic)
            songs_dic["Album ID"] = i
        # music["Songs URL"] = music_url
        # music["Songs"] = music_url
    return music_url

    # content.append(music)

if __name__ == "__main__":
    song = pd.read_excel("movie_url.xlsx",index_col=None)["movie"].to_list()
    movie = movie_details(song[:50])

    movies = pd.DataFrame(movie)
    movies = movies[["Album", "Actors", "Directed by", "Produced by", "Music Director", "Language","Release Date", "Image"]]

    # Export DataFrame to Excel
    excel_file = 'movies.xlsx'
    movies.to_excel(excel_file, index=False)

    music = song_details(song[:50])

    musics =pd.DataFrame(music)
    musics = musics[["Album ID","Album", "Song Name", "Duration", "Singers", "Song URL"]]
    excel_file = "songs.xlsx"
    musics.to_excel(excel_file,index=False)
    

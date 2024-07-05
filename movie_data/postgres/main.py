from config import config
import psycopg2
import pandas as pd
from pathlib import Path
import os

def connect(songs,albums):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        crusor = connection.cursor()
        connection.autocommit = True
        print("connection sucessful")
        crusor.execute("SELECT album FROM music_albums ;")
        al = crusor.fetchall()
        ab=[]
        for a in al:
            ab.append(a[0])
        post(crusor,songs=songs,albums=albums,ab=ab)
        print("Database created")
    except Exception as e:
        print(e)
    finally:
        if connection is not None :
            connection.close()
            print('connection ended')


def post(crusor,songs,albums,ab):
#     album_table = """
#         id SERIAL PRIMARY KEY,
#         Album VARCHAR(200),
# """
#     song_table = """CREATE TABLE IF NOT EXISTS 'songs' (
#         id SERIAL PRIMARY KEY ;
#         Album VAR
#     )"""

    for i , row in albums.iterrows():
        if row["Album"] not in ab:
            crusor.execute("""
                        INSERT INTO music_albums (album,actors,directed_by,produced_by,music_directors,language,release_date,image_url)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ;
                        """,(row["Album"],row["Actors"],row['Directed by'],row['Produced by'],row['Music Director'],row['Language'],row['Release Date'],row['Image'])) 
        else:
            print(f"{row['Album']}exist")
    for i , row in songs.iterrows():
        if row["Album"] not in ab:    
            crusor.execute("""
                        INSERT INTO music_songs (album_id,song_name,singers,durations,song_url)
                        VALUES (%s,%s,%s,%s,%s) ;
                        """,(row["Album"],row["Song Name"],row['Singers'],row['Duration'],row['Song URL'])) 
        else:
            print(f"{row['Album']}exist")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_1 = os.path.join(BASE_DIR,"songs.xlsx")
    file_2 = os.path.join(BASE_DIR,"movies.xlsx")
    df1 = pd.read_excel(file_1)
    df2 = pd.read_excel(file_2)
        
    connect(songs=df1,albums=df2)
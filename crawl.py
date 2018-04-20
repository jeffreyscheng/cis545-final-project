import pandas as pd
import requests
import lyricsgenius as genius
import spotipy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

genius_client_id = 'Qeii-UKMUUwsAYCuuemsF7CZk7R2bFDhjP1FMkqpozASvYsA4wQDlLmd2JFM3Vhm'
genius_secret_id = 'fWhV7VtwAL-5D32Ga9Y0Kyh_VFEo7XK0Jf8-3RMcZ5EoMXqsDpmFWFFPyobnibfMXJuJ-GZe69YEuXR-36VGAA'
genius_client_access_token = '1QVL91jZbgdOIhvYhqKku_zkFDf6MHEyLpXEITHU2tE2HGvAqYIPInTrQaWcInD7'
app_website_url = 'http://cis545genius.com'
redirect_uri = 'cis545genius.com'
base_url = 'https://api.genius.com'
# driver_path = '/Users/ericdong/Downloads/chromedriver'
driver_path = "/mnt/c/Users/jeffr/Downloads/chromedriver_win32/chromedriver.exe"
artist_url = 'https://www.ranker.com/crowdranked-list/the-greatest-rappers-of-all-time'
page_downs = 0
api = genius.Genius(genius_client_access_token)
spotify = spotipy.Spotify()


def get_artists(url, page_downs, driver_path):
    driver = webdriver.Chrome(driver_path)
    driver.get(url)
    time.sleep(1)
    page = driver.find_element_by_tag_name('body')
    for i in range(page_downs):
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    artists = driver.find_elements_by_class_name('listItem__data')
    names = [artist.find_element_by_class_name('listItem__title').text for artist in artists[:-1]]
    driver.quit()
    
    return names


def get_songs(artist):
    return api.search_artist(artist, verbose=False, max_songs=2)


artists = get_artists(artist_url, page_downs, driver_path)


print(artists)


music = []
for artist in artists:
    try:
        music = music + get_songs(artist).songs
    except AssertionError:
        pass


print(music)


df = pd.DataFrame()
df['artist'] = list(map(lambda x: x.artist, music))
df['song'] = list(map(lambda x: x.title, music))
df['album'] = list(map(lambda x: x.album, music))
df['lyrics'] = list(map(lambda x: x.lyrics, music))
print(df.head())

df.to_csv('genius.csv')

spotify = spotipy.Spotify()
spotify_artists = [spotify.search(q='artist:' + artist, type='artist') for artist in artists]
print(spotify_artists)
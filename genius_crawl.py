# import sys
# get_ipython().system('{sys.executable} -m pip install lyricsgenius')
# get_ipython().system('{sys.executable} -m pip install spotipy')
# get_ipython().system('{sys.executable} -m pip install selenium')
import pandas as pd
import requests
import lyricsgenius as genius
import spotipy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[7]:

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


# In[8]:

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


# In[9]:

def get_songs(artist):
    return api.search_artist(artist, verbose=False, max_songs=2)


# In[11]:

artists = get_artists(artist_url, page_downs, driver_path)


# In[68]:

print(artists)


# In[69]:

music = []
for artist in artists:
    try:
        music = music + get_songs(artist).songs
    except AssertionError:
        pass


# In[79]:

print(music)


# In[107]:

df = pd.DataFrame()
df['artist'] = list(map(lambda x: x.artist, music))
df['song'] = list(map(lambda x: x.title, music))
df['album'] = list(map(lambda x: x.album, music))
df['lyrics'] = list(map(lambda x: x.lyrics, music))
print(df.head())


# In[37]:

# headers = {'Authorization': 'Bearer %s' % genius_client_access_token}
# search_url = base_url + '/search'
# song_title = 'Mercy'
# params = {'q': song_title}
# response = requests.get(search_url, params=params, headers=headers)
# json = response.json()
# print(json)


# In[ ]:

df.to_csv('genius.csv')


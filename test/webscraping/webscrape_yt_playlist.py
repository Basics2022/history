"""
Webscrape Youtube page of a playlist
"""

import re
import requests
from bs4 import BeautifulSoup

# URL of the YouTube playlist
# scrip. Corso di storia
url = 'https://www.youtube.com/playlist?list=PLFRYVVEHvMSxS14eeI8c9RIfRleHl6vTi'
substring = '"title":{"runs":[{"text"'   # string before the title of the videos
substring = re.escape(substring)

# find_string = 'title"'

# substring = 'sndlas'
# soup_str = 'sndlassndlas,sndlasjipsndlashlsndlashlutifisndlas'

# Fetch the content of the webpage
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    soup_str = str(soup)

    with open('output.html', 'w') as f:
        f.write(soup_str)

    matches = re.finditer(substring, soup_str)
    print(matches)
    for match in matches:
        print(f"match at position {match.start()}")

    # # Find all elements containing video titles
    # # video_titles = soup.find_all('a', class_='pl-video-title-link')
    # video_titles = soup.find_all('a', class_='ytd-playlist-video-renderer')

    # if video_titles:
    #     for title in video_titles:
    #         # Print the titles
    #         print(title.text.strip())

    # else:
    #     print("No video titles found.")
else:
    print("Failed to retrieve the webpage.")
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import shutil


# set the base URL for the Figma file
url = 'https://www.reddit.com/r/ThisAmericanLife/wiki/download/'

# saved folder path
folder_path = "/Users/dangercat/Documents/GitHub/this-americon-life-episode-downloader/episodes"

# chrome options
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": folder_path}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
# navigate to the login page
driver.get(url)

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

### Search
# Search for the specific download links
download_links = []
episode_titles = []

# Replace 'keyword' with the desired keyword that you want to search for in the links
episode_file_extention = '.mp3'
link_title_url = 'tal.fm'
        
# Find all 'td' elements in the HTML document
td_elements = soup.find_all('td')

for td in td_elements:
    link_list = td.find_all('a')
    for link in link_list:
        if (link.text == 'DL'):
            download_links.append(link.get('href'))
        elif (link_title_url in link.get('href')):
            episode_titles.append(link.text)

print(len(download_links))
print(len(episode_titles))

i = 0

# Download the files
for dl_link in download_links:

    # make a GET request to the URL and stream the response content
    response = requests.get(download_links[i], stream=True)
    
    # open a local file to write the MP3 content to
    try:
        if not os.path.exists(f'episodes/{episode_titles[i]}.mp3'):
            with open(f'episodes/{episode_titles[i]}.mp3', 'wb') as f:
                print(f"Downloading: {episode_titles[i]}")
                # iterate over the response content by chunk and write to file
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Skipping: {episode_titles[i]} (file already exists)")
            
    except FileNotFoundError as g:
        print(f'episode {episode_titles[i]} can not be downloaded')

    i += 1

print("Download complete.")

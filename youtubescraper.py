
# Importing Libraries:
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from random import randint

# Setting up selenium/smartproxy settings
HOSTNAME = 'ca.smartproxy.com'
PORT = '20001'
options = ChromeOptions()
proxy_str = '{hostname}:{port}'.format(hostname=HOSTNAME, port=PORT)
options.add_argument('--proxy-server={}'.format(proxy_str))
scroll_pause_low = 0
scroll_pause_high = 3

url = "https://www.youtube.com/@TorontoSymphony/videos"

# Starting Browser with smartproxy, opening up Videos page:
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                           options=options)
browser.get(url)

df = pd.DataFrame(columns=["Title", "Length", "Days Ago", "Link"])

# Scroll all the way down:
## Did this manually for now.

    
# Title, Length and Date: "yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media"
elements_titlelengthdate = browser.find_elements(by=By.CLASS_NAME, value="style-scope ytd-rich-grid-media")
# URL links: "video-title-link"
elements_link = browser.find_elements(by=By.ID, value="video-title-link")


# Check if lengths of two elements lists are the same:
if len(elements_titlelengthdate) != len(elements_link):
    print("Error, URLS and Titles not in same number")

# Cycle through elements and add relevant information to the dataframe:
for i in range(len(elements_titlelengthdate)):
    
    i_length = elements_titlelengthdate[i].text.splitlines()[0]
    i_title = elements_titlelengthdate[i].text.splitlines()[1]
    # i_views = elements_titlelengthdate[i].text.splitlines()[2]
    i_daysago = elements_titlelengthdate[i].text.splitlines()[3]
    i_link = elements_link[i].get_attribute('href')

    df.loc[i] = [i_title, i_length, i_daysago, i_link]


# Code to execute for just one link (rather than recursively over a list of links):
"""
url = "https://www.youtube.com/watch?v=-2pjLNrHka4"
browser.get(url)

# Clicking the Play button
stop_play = browser.find_element(by=By.TAG_NAME, value="ytd-player")
stop_play.click()

# Clicking the "more" button
button = browser.find_element(by=By.ID, value="expand")
button.click()

# Finding the date:
elements_dates = browser.find_elements(by=By.CLASS_NAME, value="style-scope ytd-watch-info-text")
date = elements_dates[0].text.split()[2] + " " + elements_dates[0].text.split()[3] + " " + elements_dates[0].text.split()[4]
print(date)
"""

df_dates = pd.DataFrame(columns=["Date_published"])

# Loop, go to each link in df, lookup date, continue:
for i in range(212, len(elements_titlelengthdate)):
    
    #define and get url:
    try:
        url_temp = df["Link"][i]
    except:
        print("error here 1 " + str(i))
        break
    try:
        browser.get(url_temp)
    except:
        print("error here 2 " + str(i))
        break
    # random pause:
    time.sleep(randint(scroll_pause_low, scroll_pause_high))
    #stop play and click more button
    try:    
        stop_play = browser.find_element(by=By.TAG_NAME, value="ytd-player")
        stop_play.click()
        button = browser.find_element(by=By.ID, value="expand")
        button.click()
    except:
        print("error here 3 " + str(i))
        break
    # store date:
    try:
        elements_dates = browser.find_elements(by=By.CLASS_NAME, value="style-scope ytd-watch-info-text")
    except:
        print("error here 4 " + str(i))
    date = elements_dates[0].text.split()[2] + " " + elements_dates[0].text.split()[3] + " " + elements_dates[0].text.split()[4]
    df_dates.loc[i] = [date]
    # random pause:
    time.sleep(randint(scroll_pause_low, scroll_pause_high))

print(len(df_dates))
#Export 
df_dates.to_csv('TSO_youtube_video_list.csv', index=False, encoding='utf-8')

# Merge Dataframes:
df_final = pd.concat([df, df_dates["Date_published"]], axis=1)
print(df_final)
df_final.to_csv('TSO_youtube_video_list.csv', index=False, encoding='utf-8')

# Quit browser and export df to a CSV
browser.quit()





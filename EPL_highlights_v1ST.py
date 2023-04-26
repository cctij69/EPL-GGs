from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import streamlit as st
import feedparser
import re


tableList = []
hotList = []
gamesAndLinks = {}
listOfGames = []



hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)




htp="https://raw.githubusercontent.com/cctij69/EPL-GGs/main/Footy_logo.png" 
st.image(htp, width=350)







def figureOutDate(tableList,country):
    
    target_dayofweek = 0  
    current_dayofweek = datetime.datetime.now().weekday() # Today


    if target_dayofweek <= current_dayofweek:
        # target is in the current week
        #endDate = datetime.datetime.now() - datetime.timedelta(current_dayofweek - target_dayofweek)
        endDate = datetime.datetime.now() - datetime.timedelta(weeks=1) + datetime.timedelta(target_dayofweek - current_dayofweek)
        endDatePlusOne = endDate + datetime.timedelta(weeks=1)

    else: 
        # target is in the previous week
        endDate = datetime.datetime.now() - datetime.timedelta(weeks=1) + datetime.timedelta(target_dayofweek - current_dayofweek)


    last_monday = f"{endDate:%Y%m%d}"
    last_mondayPlusOne = f"{endDatePlusOne:%Y%m%d}"





    url = "https://areyouwatchingthis.com/soccer/games?date={}".format(last_monday)
    getGames(tableList,url)
    url = "https://areyouwatchingthis.com/soccer/games?date={}".format(last_mondayPlusOne)
    getGames(tableList,url)

    if not hotList:
        st.write("No good games found!")
    else:
        getRSSLinks(hotList,country)

def getGames(tableList,url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
                    
    for header in soup.findAll('h3'):
        ul = header.findNext('ul')
        for test in ul.find_all('li', {'class': 'high'}):
            a_list = [test.find_all("a", {"class": "team"})]
            content = [item.text.strip() for p in a_list for item in p]
                
                
            listOfGames.append(content)

        for test in ul.find_all('li', {'class': 'severe'}):
            a_list = [test.find_all("a", {"class": "team"})]
            content = [item.text.strip() for p in a_list for item in p]
                
                
            listOfGames.append(content)    

    for item in listOfGames:
        if item[0] in tableList:
            hotList.append(item)
        elif item[1] in tableList:
            if item not in hotList:
                hotList.append(item)

def getPremTable():

   
    url = "https://www.bbc.com/sport/football/tables"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")


    entries = soup.find_all('abbr', class_='sp-u-abbr-on sp-u-abbr-off@m')
    for entry in entries[7:]:
        tableList.append(entry['title'])

def getRSSLinks(hotList,country):
    if country == 1:
        rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCD2lJITnvzflNhOqQckMpQg"
    elif country == 2:
        rss_url = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLISuFiQTdKDWuKYvHa2f4SxSQCK18dgCy"
    feed = feedparser.parse(rss_url)
    
    max_week = 0
    for entry in feed.entries[:15]:
        string = entry.title

        # Extract the week number from entry.title using a regular expression pattern
        pattern = r"\bWeek (\d+)\b"
        match = re.search(pattern, entry.title)
        if match:
            # Extract the week number from the match object and convert to integer
            week = int(match.group(1))
            # Update the max_week if the current week is higher
            if week > max_week:
                max_week = week

    if country < 2:
        for team in hotList:
            for entry in feed.entries[:15]:
                if team[0] in entry.title:
                    if team[1] in entry.title:
                        if str(max_week) in entry.title:
                            gamesAndLinks[entry.title] = entry.link
                if team[1] in entry.title:
                    if team[0] in entry.title:
                        if str(max_week) in entry.title:
                            gamesAndLinks[entry.title] = entry.link
    else:
        for team in hotList:
            for entry in feed.entries[:15]:
                if "United" in team[0]:
                    teamSplit = team[0].split(" ")
                    team[0] = teamSplit[0]
                if "United" in team[1]:
                    teamSplit = team[1].split(" ")
                    team[1] = teamSplit[0]
                if "City" in team[0]:
                    teamSplit = team[0].split(" ")
                    team[0] = teamSplit[0]
                if "City" in team[1]:
                    teamSplit = team[1].split(" ")
                    team[1] = teamSplit[0]


                if team[0] in entry.title:
                    if team[1] in entry.title:
                            gamesAndLinks[entry.title] = entry.link
                if team[1] in entry.title:
                    if team[0] in entry.title:
                            gamesAndLinks[entry.title] = entry.link

    







    st.write("******** List of Games to watch! ********")
    for key, value in gamesAndLinks.items():
        output = "{}: {}".format(key, value)
        st.write(output)





getPremTable()


if st.button("Canada"):
    country = 1
    figureOutDate(tableList,country)
if st.button("UK"):
    country = 2
    figureOutDate(tableList,country)
    












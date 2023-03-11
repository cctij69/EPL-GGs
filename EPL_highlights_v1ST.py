from bs4 import BeautifulSoup
from urllib.request import urlopen
from youtubesearchpython import *
import datetime
from colorama import Fore
import streamlit as st
import feedparser


tableList = []
hotList = []
gamesAndLinks = {}



def getGames2(tableList,dateRange):

    listOfGames = []
    #dateRange = 2
    today = datetime.date.today()



    target_dayofweek = 0  
    current_dayofweek = datetime.datetime.now().weekday() # Today


    if target_dayofweek <= current_dayofweek:
        # target is in the current week
        #endDate = datetime.datetime.now() - datetime.timedelta(current_dayofweek - target_dayofweek)
        endDate = datetime.datetime.now() - datetime.timedelta(weeks=1) + datetime.timedelta(target_dayofweek - current_dayofweek)

    else: 
        # target is in the previous week
        endDate = datetime.datetime.now() - datetime.timedelta(weeks=1) + datetime.timedelta(target_dayofweek - current_dayofweek)

    last_monday = f"{endDate:%Y%m%d}"





    if dateRange == 2:
        print ("Processing.....")
        url = "https://areyouwatchingthis.com/soccer/games?date={}".format(last_monday)
    else:
        url = "https://areyouwatchingthis.com/soccer/games"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
   


    if dateRange == 0:
        for header in soup.findAll('h3'):
            headerText = header.text
            if str(today.day) in headerText:
                ul = header.findNext('ul')
                for test in ul.find_all('li', {'class': 'high'}):
                    a_list = [test.find_all("a", {"class": "team"})]
                    content = [item.text.strip() for p in a_list for item in p]

                    listOfGames.append(content)
                
                for test in ul.find_all('li', {'class': 'severe'}):
                    a_list = [test.find_all("a", {"class": "team"})]
                    content = [item.text.strip() for p in a_list for item in p]

                    listOfGames.append(content)                    
                    
    elif dateRange > 0:
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



    getRSSLinks(hotList)
            
def getPremTable():

   
    url = "https://www.bbc.com/sport/football/tables"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")


    entries = soup.find_all('abbr', class_='sp-u-abbr-on sp-u-abbr-off@m')
    for entry in entries[7:]:
        tableList.append(entry['title'])

def getYTLinks(hotList):
    #location = int(input("0-CAN links 1-UK links \n"))
    for team in hotList:
        teamNames = team[0] + " vs " + team[1]
        search = CustomSearch((teamNames) + " on fuboTV Canada", VideoUploadDateFilter.thisWeek, limit = 1)
        for video in search.result()['result']:
            title = video['title']
            if team[0] and team[1] in title:
                gamesAndLinks[video['title']] = video['link']
            else:
                pass



    print ("\n***** List of Games to watch! *****n")
    st.write("******** List of Games to watch! ********")
    for key, value in gamesAndLinks.items():
        print ("\033[0m{}: \033[1;32m{}".format(key, value))
        test = "{}: {}".format(key, value)
        st.write(test)
    print ("\n")
    #st.write("\n")

def getRSSLinks(hotList):
    rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCD2lJITnvzflNhOqQckMpQg"
    feed = feedparser.parse(rss_url)
    
    
    
    
    for team in hotList:
        for entry in feed.entries[:15]:
            if team[0] and team[1] in entry.title:
                #print(entry.title, entry.link)
                gamesAndLinks[entry.title] = entry.link

    st.write("******** List of Games to watch! ********")
    for key, value in gamesAndLinks.items():
        test = "{}: {}".format(key, value)
        st.write(test)
  





getPremTable()

if st.button("Today"):
    dateRange = 0
    getGames2(tableList,dateRange)

if st.button("This week"):
    dateRange = 1
    getGames2(tableList,dateRange)


if st.button("Last week"):
    dateRange = 2
    getGames2(tableList,dateRange)
    












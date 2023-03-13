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
dateRange = 0

def figureOutDate(tableList,dateRange):
    
    today = datetime.date.today()
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






    if dateRange == 2:
        print ("Processing.....")
        url = "https://areyouwatchingthis.com/soccer/games?date={}".format(last_monday)
        getGames(tableList,url,dateRange,today)
        url = "https://areyouwatchingthis.com/soccer/games?date={}".format(last_mondayPlusOne)
        getGames(tableList,url,dateRange,today)
        return dateRange

    else:
        url = "https://areyouwatchingthis.com/soccer/games"
        getGames(tableList,url,dateRange,today)
        return dateRange

def getGames(tableList,url,dateRange,today):
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

def getPremTable():

   
    url = "https://www.bbc.com/sport/football/tables"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")


    entries = soup.find_all('abbr', class_='sp-u-abbr-on sp-u-abbr-off@m')
    for entry in entries[7:]:
        tableList.append(entry['title'])

def getRSSLinks(hotList,dateRange):
    rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCD2lJITnvzflNhOqQckMpQg"
    feed = feedparser.parse(rss_url)
    
    listOfWeeks=[]
    for entry in feed.entries[:15]:
        string = entry.title
        pattern = r"(?<=\|).*?(?=\|)"
        match = max(re.findall(pattern, string), key=lambda x: int(re.sub(r'\D', '', x)))
        listOfWeeks.append(match)
    max_num = max(map(lambda x: int(re.findall('\d+', x)[0]), listOfWeeks))
    
    
    for team in hotList:
        for entry in feed.entries[:15]:
            if dateRange == 2:
                if team[0] and team[1] in entry.title:
                    gamesAndLinks[entry.title] = entry.link
            else:
                if team[0] and team[1] in entry.title:
                    if str(max_num) in entry.title:
                        gamesAndLinks[entry.title] = entry.link




    st.write("******** List of Games to watch! ********")
    for key, value in gamesAndLinks.items():
        test = "{}: {}".format(key, value)
        st.write(test)





getPremTable()


if st.button("Today"):
    dateRange = 0
    dateRange = figureOutDate(tableList,dateRange)

if st.button("This week"):
    dateRange = 1
    dateRange = figureOutDate(tableList,dateRange)


if st.button("All recent"):
    dateRange = 2
    dateRange = figureOutDate(tableList,dateRange)
    

if not hotList:
    print("No good games found!")
else:
    getRSSLinks(hotList,dateRange)










from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import streamlit as st
import feedparser
import re
import requests


tableList = []
hotList = []
gamesAndLinks = {}
listOfGames = []
content = []



hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)




htp="https://raw.githubusercontent.com/cctij69/EPL-GGs/main/Footy_logo.png" 
st.image(htp, width=350)






def calculateGGs(country):

    url = "https://www.soccerstats.com/results.asp?league=england&pmtype=round98"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    request = Request(url, headers=headers)

    page = urlopen(request)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    matchweek_table = soup.find('table', id='btable')
    # Check if the table exists
    if matchweek_table:
        rows = matchweek_table.find_all('tr')

        for row in rows[1:]:  # Skip the first row since it contains headers
            goodGame = False
            content = []
            columns = row.find_all('td')
            if len(columns) >= 9:  # Make sure the row has at least 9 columns
                date = columns[0].text.strip()
                team1 = columns[1].text.strip()
                score = columns[2].text.strip()
                team2 = columns[3].text.strip()
                tg = columns[7].text.strip()
                link = columns[4].find('a')['href']  # Get the link URL
                linkText = columns[4].find('a').string

                if "stats" in linkText: # To check if the game has started
                    # Now, make a request to the linked URL
                    link = "http://www.soccerstats.com/"+link
                    request = Request(link, headers=headers)

                    linked_page = urlopen(request)
                    linked_html = linked_page.read().decode("ISO-8859-1")
                    linked_soup = BeautifulSoup(linked_html, "html.parser")


                    # Find the surprise rating on the linked page
                    b_elements = linked_soup.find_all('b')
                    target_text = "Outcome surprise-level"
                    target_index = None
                    for index, element in enumerate(b_elements):
                        if element.text.strip() == target_text:
                            target_index = index
                            break

                    # Get the value after the target element if it exists
                    surpriseValue = None
                    if target_index is not None and target_index + 1 < len(b_elements):
                        surpriseValue = b_elements[target_index + 1].text.strip()




                # Check for any cards
                yellow_cards = linked_soup.find_all('img', src='img/football/yellow.png')
                count_yellow_images = len(yellow_cards)
                red_cards = linked_soup.find_all('img', src='img/football/red.png')
                count_red_images = len(red_cards)

                tags = []

                # Calculate good games
                if int(tg) > 2:
                    goodGame = True
                    tags.append("Goals!")
                if surpriseValue is None:
                    pass
                else:                    
                    if int(float(surpriseValue)) > 49:
                        goodGame = True
                        tags.append("Surprising result!")  
                if count_red_images > 0:
                    st.write("YES!")
                    goodGame = True
                    tags.append("Red card!")
                
                content.append(team1)
                content.append(team2)
                content.append(' '.join(tags))
                if goodGame == True:
                    hotList.append(content)

                    

    getRSSLinks(hotList,country)



#                print(f"Date: {date}")
#                print(f"Team 1: {team1}")
#                print(f"Team 2: {team2}")
#                print(f"Score: {score}")
#                print(f"TG: {tg}")
#                print(f"Number of yellow cards: {count_yellow_images}")
#                print(f"Number of red cards: {count_red_images}")
#                print(f"Outcome surprise level: {surpriseValue}")
#                if goodGame == True:
#                    print("Good Game!")
#                print("---------------------")
#    else:
#        print("Matchweek table not found on the webpage.")







def getRSSLinks(hotList,country):
    if country == 1:
        rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCD2lJITnvzflNhOqQckMpQg"
    elif country == 2:
        rss_url = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLISuFiQTdKDVc889y-twg_gfR55muAAbT"
    feed = feedparser.parse(rss_url)
    


    if country < 2:
        for team in hotList:
            for entry in feed.entries[:15]:
                if "Utd" in team[0]:
                    teamSplit = team[0].split(" ")
                    team[0] = teamSplit[0]
                if "Utd" in team[1]:
                    teamSplit = team[1].split(" ")
                    team[1] = teamSplit[0]
                if team[0] in entry.title:
                    if team[1] in entry.title:
                        #gamesAndLinks[entry.title] = entry.link
                        gamesAndLinks[entry.title] = {team[2]: entry.link}

                if team[1] in entry.title:
                    if team[0] in entry.title:
                        #gamesAndLinks[entry.title] = entry.link
                        gamesAndLinks[entry.title] = {team[2]: entry.link}

    else:
        for team in hotList:
            for entry in feed.entries[:15]:
                if "United" in team[0]:
                    teamSplit = team[0].split(" ")
                    team[0] = teamSplit[0]
                if "United" in team[1]:
                    teamSplit = team[1].split(" ")
                    team[1] = teamSplit[0]
                if "Utd" in team[0]:
                    teamSplit = team[0].split(" ")
                    team[0] = teamSplit[0]
                if "Utd" in team[1]:
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
                            #gamesAndLinks[entry.title] = entry.link
                            gamesAndLinks[entry.title] = {team[2]: entry.link}

                if team[1] in entry.title:
                    if team[0] in entry.title:
                            #gamesAndLinks[entry.title] = entry.link
                            gamesAndLinks[entry.title] = {team[2]: entry.link}
    







    st.write("******** List of Games to watch! ********")
    for key, value in gamesAndLinks.items():
        #output = "{}: {}".format(key, value)
        st.write(key)
        for sub_key, sub_value in value.items():
            output = "{}: {}".format(sub_key, sub_value)
            #st.write(output)
            st.write("<b>{}</b> : {}".format(sub_key, sub_value),unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")

    







if st.button("Show Links"):
    country = 1
    calculateGGs(country)
#if st.button("UK"):
#    country = 2
#    calculateGGs(country)
    












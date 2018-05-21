__author__ = "Laurence Elliott"

from urllib.request import urlopen as uOpen
from bs4 import BeautifulSoup as soup
import re
import os

# associates the windows clear terminal command with a simpler name
clear = lambda: os.system('cls')

# this script scrapes the list of all steam products (including bundles, games,
# videos, music, and software)
# at 'https://store.steampowered.com/search/?sort_by=Name_ASC',
# and calculates the current mean user rating of all the products
# on the steam platform.

my_url = "https://store.steampowered.com/search/?sort_by=Name_ASC"

# opening connection and downloading the page
uClient = uOpen(my_url)
page_html = uClient.read()
uClient.close()

# instantiating html parser
page_soup = soup(page_html, "html.parser")

# gets all steam games on the page
games = page_soup.findAll("a",{"class":"search_result_row"})

# creates an empty array which is later populated with values for product review scores
reviewScores = []

# creates an integer value for the last catalogue page number
lastPageNum = 0
pageNumTags = page_soup.findAll("a", {"onclick":"SearchLinkClick( this ); return false;"})
for pageNumTag in pageNumTags:
    pageNum = re.search('(?<=return false;">).*(?=</a>)', str(pageNumTag)).group(0)
    if len(pageNum) > 3 and pageNum != "&gt;":
        lastPageNum = pageNum


def appendScores():
    for i in range(0, len(games) - 1):
        try:
            try:
                reviewSpanTag = str(games[i].findAll("span", {"class": "search_review_summary positive"})[0]["data-tooltip-html"])
                reviewScores.append(int(re.search('(?<=<br>).*(?=%)', reviewSpanTag).group(0)))
            except:
                reviewSpanTag = str(games[i].findAll("span", {"class": "search_review_summary negative"})[0]["data-tooltip-html"])
                reviewScores.append(int(re.search('(?<=<br>).*(?=%)', reviewSpanTag).group(0)))
        except:
            print("Excluded product without review score")


for i in range (0, int(lastPageNum)-1):
    if i == 0:
        appendScores()
    else:
        my_url = "https://store.steampowered.com/search/?sort_by=Name_ASC&page=2" + str(i)

        # opening connection and downloading the page
        uClient = uOpen(my_url)
        page_html = uClient.read()
        uClient.close()

        # instantiating html parser
        page_soup = soup(page_html, "html.parser")

        # gets all steam games on the page
        games = page_soup.findAll("a", {"class": "search_result_row"})

        appendScores()
    clear()
    print(str(round((((i+1)/int(lastPageNum)) * 100), 2)) + "% of catalogue pages parsed")

scoresTotal = 0
for i in range (0,len(reviewScores)-1):
    scoresTotal += reviewScores[i]
steam_mean = str(round(scoresTotal/(len(reviewScores)), 2))
print("\n" + str(lastPageNum) + " pages parsed"
"\nMean steam product review score: " + steam_mean + "%")
with open('steam_mean.txt','w+') as file:
    file.write(steam_mean)
print("\nValue stored in 'steam_mean.txt'")


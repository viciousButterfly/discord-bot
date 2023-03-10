import requests
from bs4 import BeautifulSoup
import os
import random


"""
Fetch articles by 
scrapping websites using BeatifulSoup
"""
class Article:

    def itsfoss():
        try:
            # Making a GET request
            r = requests.get('https://itsfoss.com/')

            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Find articles
            s = soup.find_all('article')

            # Take random article
            article = s[random.randint(0,len(s)-1)]

            # Find img tag for title
            img = article.find('img')
            alt = img.get('alt')

            # # Find a tag for link
            a = article.find('a')
            href = a.get('href')

            # return alt,href
            return alt, href if href[0]=="h" else "https://itsfoss.com"+href
        
        except:
            # Couldn't fetch articles
            return False

    def omgubuntu():
        try:
            # Making a GET request
            r = requests.get('https://www.omgubuntu.co.uk/category/news')


            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')

            # Find divs
            s = soup.find_all('div',class_='sbs-layout__item')

            # Find random article
            article = s[random.randint(0,len(s)-1)]

            # Find a tag for link
            a = article.find('a', class_='layout__title-link')

            # Find alt and href
            alt = a.text
            href = a.get('href')

            return alt,href
        
        except:
            # Couldn't fetch articles
            return False

    def phoronix():
        try:
            # Making a GET request
            r = requests.get('https://www.phoronix.com/news')

            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')

            #Find all popular divs
            div = soup.find_all('div',class_='popular-list')

            # Take random article
            article = div[random.randint(0,len(div)-1)]

            # Find a tag from article
            a = article.find('a')

            # Find alt and href
            alt = a.text
            href = a.get('href')

            return alt,"https://www.phoronix.com"+href
        
        except:
            # Couldn't fetch articles
            return False


"""
Fetch information
using APIs related to the query
"""
class API:

    def github(arg):
        try:
            # Making a GET request
            r = requests.get(url='https://api.github.com/search/repositories?q={}&page=1&per_page=5'.format(arg))

            # Extracting json
            data = r.json()

            # Extracting name and url from json
            count = 0
            repos = []
            for i in range(0,5) :
                if count >= data["total_count"]:
                    break
                repos.append((data["items"][i]["full_name"],data["items"][i]["html_url"]))
                count+=1

            return repos

        except:
            # Couldn't fetch repositories
            return False

    def youtube(arg):
        try:
            # Making a GET request
            r = requests.get(url='https://www.googleapis.com/youtube/v3/search?key={}&part=snippet&type=video&maxResults=1&q={}'.format(os.getenv("API_KEY"),arg))

            # Extracting JSON
            data = r.json()

            # Extracting videoID
            videoId = data["items"][0]["id"]["videoId"]

            return f"https://youtube.com/watch?v={videoId}"
        
        except:
            # Couldn't fetch videos
            return False

    def dictionary(arg):

        try:
            # Making a GET request
            r = requests.get(url="https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(arg))

            # Extracting JSON
            data = r.json()
            
            # Extracting word and meaning
            word = data[0]["word"]
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            
            return word,meaning
        
        except:
            # Couldn't fetch meaning of the word
            return False,False

import requests
from bs4 import BeautifulSoup
import os

def itsfoss():

    # Making a GET request
    r = requests.get('https://itsfoss.com/all-blog-posts/')

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Find articles
    s = soup.find('article')

    # Find img tag for title
    img = s.find('img',class_="attachment-medium_large")
    alt = img.get('alt')

    # Find a tag for link
    a = s.find('a',class_="post-more-link")
    href = a.get('href')

    return alt,href

def github(arg):

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

def youtube(arg):

    # Making a GET request
    r = requests.get(url='https://www.googleapis.com/youtube/v3/search?key={}&part=snippet&type=video&maxResults=1&q={}'.format(os.getenv("API_KEY"),arg))

    # Extracting JSON
    data = r.json()

    # Extracting videoID
    videoId = data["items"][0]["id"]["videoId"]

    return f"https://youtube.com/watch?v={videoId}"

def dictionary(arg):

    # Making a GET request
    r = requests.get(url="https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(arg))

    # Extracting JSON
    data = r.json()
    
    # Extracting word and meaning
    try:
        word = data[0]["word"]
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        return word,meaning
    except:
        return False,False

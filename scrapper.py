import requests
from bs4 import BeautifulSoup
 

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




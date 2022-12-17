import requests

def scrape(arg):

    # Making a GET request
    r = requests.get(url='https://api.github.com/search/repositories?q={}'.format(arg))

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

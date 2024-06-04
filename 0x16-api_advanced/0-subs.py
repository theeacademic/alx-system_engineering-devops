#!/usr/bin/python3
import requests

def number_of_subscribers(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {'User-Agent': 'custom-user-agent/0.1'}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data['data']['subscribers']
        elif response.status_code == 404:
            return 0
        else:
            return 0
    except requests.RequestException as e:
        return 0
subreddit = "python"
print(f"Number of subscribers in r/{subreddit}: {number_of_subscribers(subreddit)}")

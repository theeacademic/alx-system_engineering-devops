#!/usr/bin/python3
import requests

def recurse(subreddit, hot_list=[], after=None):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'custom-user-agent/0.1'}
    params = {'limit': 100}
    if after:
        params['after'] = after
    
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            children = data['data']['children']
            for child in children:
                hot_list.append(child['data']['title'])
            after = data['data']['after']
            if after:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        elif response.status_code == 404:
            return None
        else:
            return None
    except requests.RequestException as e:
        return No
subreddit = "python"
hot_titles = recurse(subreddit)
if hot_titles is not None:
    print(f"Hot articles in r/{subreddit}:")
    for title in hot_titles:
        print(title)
else:
    print(f"No hot articles found for r/{subreddit} or the subreddit is invalid.")


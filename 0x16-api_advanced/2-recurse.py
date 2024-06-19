#!/usr/bin/python3
"""
This module contains a recursive function to query the Reddit API and return
a list containing the titles of all hot articles for a given subreddit.
"""

import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list, optional): List to store the titles of hot articles. Defaults to [].
        after (str, optional): Parameter for pagination. Defaults to None.

    Returns:
        list: A list containing the titles of all hot articles for the subreddit,
              or None if the subreddit is invalid or no results are found.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}
    
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            
            # Extract titles and add to hot_list
            for post in posts:
                hot_list.append(post['data']['title'])
            
            # Check for pagination (next page)
            after = data['data'].get('after')
            if after:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return None
    except requests.RequestException:
        return None

if __name__ == "__main__":
    subreddit = "python"
    result = recurse(subreddit)
    if result:
        for title in result:
            print(title)
    else:
        print(f"No hot articles found for subreddit '{subreddit}' or subreddit is invalid.")


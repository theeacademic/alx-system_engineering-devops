#!/usr/bin/python3
"""
This module contains a recursive function to query the Reddit API, parse the titles
of all hot articles, and print a sorted count of given keywords.
"""

import requests
import re

def count_words(subreddit, word_list, count_dict=None, after=None):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count occurrences of.
        count_dict (dict, optional): Dictionary to store counts of keywords. Defaults to None.
        after (str, optional): Parameter for pagination. Defaults to None.

    Returns:
        None
    """
    if count_dict is None:
        count_dict = {}
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}
    
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            
            # Extract titles and count keywords
            for post in posts:
                title = post['data']['title'].lower()
                for word in word_list:
                    # Use regex to find whole words (not substrings)
                    matches = re.findall(r'\b' + re.escape(word.lower()) + r'\b', title)
                    count_dict[word.lower()] = count_dict.get(word.lower(), 0) + len(matches)
            
            # Check for pagination (next page)
            after = data['data'].get('after')
            if after:
                return count_words(subreddit, word_list, count_dict, after)
            else:
                # Sort count_dict by count (descending), then alphabetically (ascending)
                sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
                
                # Print results
                for word, count in sorted_counts:
                    print(f"{word}: {count}")
        else:
            print(None)
    except requests.RequestException:
        print(None)

if __name__ == "__main__":
    subreddit = "python"
    word_list = ["python", "java", "javascript"]
    count_words(subreddit, word_list)


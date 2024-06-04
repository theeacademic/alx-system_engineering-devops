#!/usr/bin/python3
import requests
from collections import Counter

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = Counter()

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
                title = child['data']['title'].lower().split()
                for word in word_list:
                    word_lower = word.lower()
                    counts[word_lower] += title.count(word_lower)
            after = data['data']['after']
            if after:
                return count_words(subreddit, word_list, after, counts)
            else:
                return counts
        elif response.status_code == 404:
            return counts
        else:
            return counts
    except requests.RequestException as e:
        return counts

def print_sorted_counts(subreddit, word_list):
    counts = count_words(subreddit, word_list)
    if not counts:
        return
    
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    for word, count in sorted_counts:
        if count > 0:
            print(f"{word}: {count}")

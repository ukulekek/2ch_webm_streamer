#!/usr/bin/env python3

import re
import sys
import json
from urllib import request
import os

path = os.path.dirname(os.path.realpath(__file__))


#GET request to get JSON site
def getRequest(url):
    with request.urlopen(url) as answer:
        return json.loads(answer.read())


# get all /b/ webm or mp4 threads
def get_webm_threads():
    catalog = {}
    catalog = getRequest('https://2ch.hk/b/catalog.json')
    threads = catalog['threads']
    webmThreads = [val for val in threads if re.search("([цшw][уэe][ибb][ьмm]|[мm][пp]4)", val['subject'], re.I) != None]

    return webmThreads

# download webm thread and parse it files
def download_thread(link):
    posts = getRequest(link)['threads'][0]['posts']
    files = []
    for post in posts:
        for file in post['files']:
            duration = 0
            if 'duration_secs' in file:
                duration = file['duration_secs']
            fileName =file['name']
            if(fileName[-3:] == 'mp4' or fileName[-4:] == 'webm'):
                files.append({"name": file['fullname'], "path": file['path'], "duration": duration, "thumbnail": file['thumbnail']})

    return files


def load_favourites():
    with open('{}/favourite.json'.format(path), 'r') as json_file:
        favourite_json = json.load(json_file)
        return favourite_json

def save_to_favourite(file):
    favourite_json = load_favourites()
    favourite_json.append(file)
    with open('{}/favourite.json'.format(path), 'w') as json_file:
        json.dump(favourite_json, json_file)

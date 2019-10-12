#!/usr/bin/env python3

import re
import sys
import json
from urllib import request


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
                files.append({"name": file['fullname'], "path": file['path'], "duration": duration})

    return files


def generate_json_playlist(files):
    json_playlist = json.dumps(files, ensure_ascii=False, indent="\t")
    return json_playlist


#if __name__ == '__main__':
#    threads = getWebmThreads()
#    printThreads(threads)
#    num = readThreadNum(0, len(threads) - 1)
#    threadLink = "https://2ch.hk/b/res/" + threads[num]['num'] + ".json"
#    files = dowloadThread(threadLink)
#    generateJsonPlaylist(files)

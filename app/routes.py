import os
from app import app
from flask import render_template, request, url_for

from app.dvach.generatePlaylist import get_webm_threads, download_thread, save_to_favourite, load_favourites

@app.route('/')
@app.route('/index')
def index():
    favourite_count = len(load_favourites())
    return render_template('index.html',
                           threads= get_webm_threads(),
                           cnt= favourite_count
                           )

@app.route('/thread/<num>', methods=["GET", "POST"])
def thread(num):
    link = "https://2ch.hk/b/res/{}.json".format(num)
    if num == 'favourite':
        files = load_favourites()
        files = files[::-1]
    else:
        files = download_thread(link)
    if request.method == 'POST':
        for form in request.form:
            if form.startswith('/b/'):
                print(form)
                add_to_favorite(form, files)
    return render_template('thread.html',
                            files= files,
                            num= num)

def add_to_favorite(path, files):
    for file in files:
        if file['path'] == path:
            save_to_favourite(file)


import os
from app import app
from flask import render_template, request, url_for

from app.dvach.generatePlaylist import get_webm_threads, download_thread, generate_json_playlist

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           threads= get_webm_threads()
                           )

@app.route('/thread/<num>')
def thread(num):
    link = "https://2ch.hk/b/res/{}.json".format(num)
    files = download_thread(link)
    return render_template('thread.html',
                            files= files)


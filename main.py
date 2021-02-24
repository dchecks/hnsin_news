from datetime import datetime
from multiprocessing.pool import ThreadPool

from flask import Flask, render_template, send_from_directory
from flask_caching import Cache
import requests

from article import Article

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/%s.json'
config = {
    # "DEBUG":                 True,  # some Flask specific configs
    "CACHE_TYPE":            "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}



app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

with open("blacklist.txt") as f:
    black_list = [line.strip() for line in f]
print("Blacklist contained %s items" % len(black_list))


@app.route('/hello')
@cache.cached(timeout=60)
def hello_world():
    return str(datetime.utcnow())

tp = ThreadPool

@app.route('/')
@cache.cached(timeout=180)
def article_list():
    hn_ids = requests.get(TOP_URL).json()
    articles = []
    for aid in hn_ids:

        article = hn_fetch_article(aid)
        if article is None:
            continue
        elif article.site not in black_list:
            articles.append(article)
            if len(articles) == 30:
                break

    return render_template('article_list.html', articles=articles)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "y18.gif")


def hn_fetch_article(hn_id):
    """ Fetch the meta data from the hn api """
    try:
        article_info = requests.get(ITEM_URL % hn_id).json()
        if article_info is None:
            return None
        if article_info.get('type') != 'story':
            return None #TODO

        url = article_info.get('url')
        title = article_info.get('title')
        if not title:
            title = ''

        submitter_id = article_info.get('by')

        article = Article(
                hn_id=hn_id,
                title=title,
                article_url=article_info.get('url'),
                score=article_info.get('score'),
                number_of_comments=article_info.get('descendants'),
                submitter=submitter_id,
                timestamp=article_info.get('time')

        )
        return article
    except Exception as e:
        raise e

# 35 of article_list <td class="title"><a href="{{ base_path }}{{ page_number|add:1 }}" class="morelink" rel="nofollow">More</a></td>
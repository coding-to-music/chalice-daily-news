from chalice import Chalice
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

news_url = "https://news.google.com/news/rss"
app = Chalice(app_name='daily-news')

@app.route('/')
def index():
    news = get_news_from_google()
    return {'result': news}


@app.route('/news')
def index():
    news = get_news_from_google()
    return {'result': news}


def get_news_from_google():
    client = urlopen(news_url)
    page = client.read()
    client.close()
    souped = soup(page, "xml")
    news_list = souped.findAll("item")
    result = []
    for news in news_list:
        data = {}
        data['title'] = news.title.text
        data['date'] = news.pubDate.text
        result.append(data)
    return result
# from chalice import Chalice

# app = Chalice(app_name='chalice-daily-news')


# @app.route('/')
# def index():
#     return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

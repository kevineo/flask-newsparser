import feedparser
import json #parse JSON safely
import urllib # download data from web
import urllib2
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
 'cnn': 'http://rss.cnn.com/rss/edition.rss',
 'fox': 'http://feeds.foxnews.com/foxnews/latest',
 'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication") #change request.args.get to request.form.get to change between form param in POST and args params in GET
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc" #default publication is bbc
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Kuala Lumpur?MY")
    return render_template("home.html",
    articles=feed['entries'],
    weather=weather)

def get_weather(query):
   api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=<APIKEY>'
   query = urllib.quote(query)
   url = api_url.format(query)
   data = urllib2.urlopen(url).read()
   parsed = json.loads(data)
   weather = None
   if parsed.get("weather"):
       weather = {  "description":parsed["weather"][0]["description"], #"weather": ["description":"broken clouds"]
                    "temperature":parsed["main"]["temp"], #"main":{"temp":29}
                    "city":parsed["name"] #"name":"Kuala Lumpur"
                    }
   return weather

if __name__ == '__main__':
    app.run(port=5000, debug= True)
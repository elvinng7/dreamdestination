import webapp2
import jinja2
import os
import sys
import logging
import time
import json
import urllib

from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

API_KEY = "650c77ad9e074e7c91aa8cdf38ee54e1"
PLACES_API_KEY = "AIzaSyApHUjZLzg4xbbE0-DaMZSrrqnQ1DiE6lc"
YELP_API_KEY = "9h-YvamQKLnHuo_aRQWp0GONd53Bx07Q25WBJMuIPoiEePZPTHAwOPjQFO6o3N6vgSh32Fd2-AAs-lUc8NaSNOen10BxNbPBVls08lJG3B_z0ee2Ve8Z2jPidPVhW3Yx"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class Destination(object):
    def __init__(self, weather, price, transportation, length, name):
        self.weather = weather
        self.price = price
        self.transportation = transportation
        self.length = length
        self.name = name

destinations = [
    # Outside of the country
    Destination(2, 2, 4, 2, "Naples, Italy"),
    Destination(1, 2, 4, 2, "Vancouver, Canada"),
    Destination(3, 2, 4, 3, "Kauai, Hawaii"),

    # Inside the US
    Destination(1, 0, 2, 1, "Seattle, Washington"),
    Destination(3, 0, 2, 1, "Yellowstone National Park, Wyoming"),
    Destination(2, 2, 3, 2, "Mount Desert Island, Maine"),
    Destination(3, 2, 3, 2, "Traverse City, Michigan"),
    Destination(3, 2, 3, 2, "New York, New York"),
    Destination(3, 0, 2, 1, "Santa Fe, New Mexico"),

    # Inside the CA
    Destination(1, 1, 0, 0, "San Francisco, California"),
    Destination(2, 1, 0, 0, "Mountain View, California"),
    Destination(3, 0, 1, 1, "San Diego, California"),
    Destination(3, 1, 0, 0, "Santa Cruz, California"),
    Destination(2, 1, 1, 1, "Monterey, California"),
]

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/home.html")
        self.response.write(template.render())

class QuestionsPage(webapp2.RequestHandler):
    def post(self):
        template = env.get_template("templates/questions.html")
        self.response.write(template.render())

class Blog(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/blog.html")
        self.response.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/about.html")
        self.response.write(template.render())

class News(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/news.html")
        url = "https://newsapi.org/v2/top-headlines?sources=google-news&apiKey=650c77ad9e074e7c91aa8cdf38ee54e1"
        #https://newsapi.org/v2/top-headlines?sources=google-news&apiKey=650c77ad9e074e7c91aa8cdf38ee54e1"
        response = urlfetch.fetch(url)
        json_result = json.loads(response.content)
        articles = json_result["articles"]
        logging.info(articles)
        templateVars = {
            "url": url,
            "response": response,
            "articles": articles,
            "json_result": json_result,
        }
        print(json_result)
        self.response.write(template.render(templateVars))

class Contact(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/contact.html")
        self.response.write(template.render())

class ResultsPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/results.html")
        self.response.write(template.render())
    def post(self):
        template = env.get_template("templates/results.html")

        weather = int(self.request.get("question1"))
        transportation = int(self.request.get("question2"))
        price = int(self.request.get("question3"))
        length = int(self.request.get("question4"))

        min_result = None
        dream_location = "Not found"

        for destination in destinations:
            results_of_similarity = (abs(destination.weather - weather)
                                    + abs(destination.transportation - transportation)
                                    + abs(destination.price - price)
                                    + abs(destination.length - length))
            if min_result == None or min_result > results_of_similarity:
                min_result = results_of_similarity
                dream_location = destination.name

        # Getting information about the dream_location using Geonames API
        geoname_url = "http://api.geonames.org/wikipediaSearchJSON?q=" + urllib.quote(dream_location) + "&username=areetaw"
        geoname_response = urlfetch.fetch(geoname_url)
        geoname_json_result = json.loads(geoname_response.content)
        summary = geoname_json_result["geonames"][0]["summary"]

        # Getting photo reference from Google Place Search API
        places_searches_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&input=" + urllib.quote(dream_location) + "&fields=photos,name&key=AIzaSyApHUjZLzg4xbbE0-DaMZSrrqnQ1DiE6lc"

        print "places_searches_url", places_searches_url

        places_searches_response = urlfetch.fetch(places_searches_url)
        places_searches_json_result = json.loads(places_searches_response.content)
        photo_reference = places_searches_json_result["candidates"][0]["photos"][0]["photo_reference"]

        # Using photo reference to call on Places Photo API
        places_photo_url = ("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="
                            + urllib.quote(photo_reference)
                            + "&key="
                            + urllib.quote(PLACES_API_KEY))

        # Getting food places near about the dream_location using Yelp API

        templateVars = {
            "dream_location": dream_location,
            "summary": summary,
            "image_url": places_photo_url,
        }
        self.response.write(template.render(templateVars))

app = webapp2.WSGIApplication([
    ("/", HomePage),
    ("/questions", QuestionsPage),
    ("/results", ResultsPage),
    ("/blog", Blog),
    ("/about", About),
    ("/news", News),
    ("/contact", Contact),
], debug=True)

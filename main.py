import webapp2
import jinja2
import os
import sys
import logging
import time
import json

from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

API_KEY = "650c77ad9e074e7c91aa8cdf38ee54e1"

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
    Destination(3, 2, 4, 3, "Albuferia, Portugal"),
    Destination(2, 2, 4, 2, "Naples, Italy"),
    Destination(3, 2, 2, 3, "Tashkent, Uzbekistano"),
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
        url = "https://newsapi.org/v2/everything?q=travel&apiKey=650c77ad9e074e7c91aa8cdf38ee54e1"
        response = urlfetch.fetch(url)
        json_result = json.loads(response.content)
        articles = json_result["articles"]
        templateVars = {
            "url": url,
            "response": response,
            "articles": articles,
            "json_result": json_result,
        }
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

        weather = self.request.get("question1")
        weather = int(weather)

        transportation = self.request.get("question2")
        transportation = int(transportation)

        price = self.request.get("question3")
        price = int(price)

        length = self.request.get("question4")
        length = int(length)

        min_result = None
        dream_location = ""

        for destination in destinations:
            results_of_similarity = (abs(destination.weather - weather)
                                    + abs(destination.transportation - transportation)
                                    + abs(destination.price - price)
                                    + abs(destination.length - length))
            if min_result == None or min_result > results_of_similarity:
                min_result = results_of_similarity
                dream_location = destination.name

        templateVars = {
            "dream_location": dream_location,
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

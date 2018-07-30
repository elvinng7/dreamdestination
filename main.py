import webapp2
import jinja2
import os
import logging
import time
from google.appengine.api import users
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class User(ndb.Model):
    name = ndb.StringProperty()
    weather = ndb.IntegerProperty()
    transportation = ndb.StringProperty()
    cost = ndb.IntegerProperty()
    numOfPeople = ndb.IntegerProperty()

class HomePage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/home.html")
        self.response.write(template.render())

class QuestionsPage(webapp2.RequestHandler):
    def post(self):
        template = env.get_template("templates/questions.html")
        self.response.write(template.render())
        templateVars = {
            "name": name,
            "weather": weather,
            "transportation": transportation,
            "cost": cost,
            "numOfPeople": numOfPeople,
        }

class ResultsPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/results.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ("/", HomePage),
    ("/questions", QuestionsPage),
    ("results", ResultsPage)
], debug=True)

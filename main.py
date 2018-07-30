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
    def get(self):
        template = env.get_template("templates/questions.html")
        self.response.write(template.render())
    def post(self):
        template = env.get_template("templates/questions.html")
        weather = self.request.get("question1")
        transportation = self.request.get("question2")
        cost = self.request.get("question3")
        numOfPeople = self.request.get("question4")

        #
        # russia = {
        #     "weather":
        # }

        templateVars = {
            "weather": question1,
            "transportation": question2,
            "cost": question3,
            "numOfPeople": question4,
            "imgURL": imgURL,
            "dreamLocation": dreamLocation,
        }
        self.response.write(template.render(templateVars))


class ResultsPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("templates/results.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ("/", HomePage),
    ("/questions", QuestionsPage),
    ("/results", ResultsPage)
], debug=True)

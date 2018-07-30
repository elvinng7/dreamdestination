import webapp2
import jinja2
import os

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        template = env.get_template("templates/welcome.html")
        self.response.write(template.render()) #the response

class CreateHandler(webapp2.RequestHandler):
    def post(self):
        name= self.request.get('name')
        biography= self.request.get('biography')

        person = Person(name=name, biography=biography, email=email)
        person.put()

        time.sleep(2)
        time.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', CreateHandler),
>>>>>>> 5a8022637cca90f72ac97edbd81b7ce1e426f9ee
], debug=True)

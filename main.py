import cherrypy
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))

def get_year():
	year = datetime.now().year
	return ("2021-" if year > 2021 else "") + str(year)

class Root(object):
	@cherrypy.expose
	def index(self):
		template = env.get_template("index.html")
		return template.render(year = get_year())

cherrypy.quickstart(Root(), "/", "app.config")
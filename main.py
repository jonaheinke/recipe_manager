import cherrypy
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))

def get_year():
	year = datetime.now().year
	return ("2021-" if year > 2021 else "") + str(year)

#theme_names = ["light", "dark"]

class Root(object):
	@cherrypy.expose
	def index(self, t=0):
		"""if not t:
			t = 0"""
		template = env.get_template("index.html")
		return template.render(year = get_year()) #theme = theme_names[t], 

cherrypy.quickstart(Root(), "/", "app.config")
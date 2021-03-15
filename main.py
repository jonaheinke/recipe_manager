import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader("templates"))

class Root(object):
	def get_darkmode(self):
		if "darkmode" in cherrypy.request.cookie and cherrypy.request.cookie["darkmode"].value in (1, "1", "true"):
			return {"int": 1, "str": "dark", "checked": "checked"}
		else:
			return {"int": 0, "str": "", "checked": ""}
	
	def render_page(self, path, **kwargs):
		assert(isinstance(path, str))
		template = env.get_template(path)
		return template.render(darkmode = self.get_darkmode(), **kwargs)
	
	@cherrypy.expose
	def index(self):
		return self.render_page("html/index.html")
	
	@cherrypy.expose
	def view(self):
		return self.render_page("html/view.html")

cherrypy.quickstart(Root(), config = "app.config")
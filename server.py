# -------------------------------------------------------------------------------------------------------------------- #
#                                                        IMPORT                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
import os, cherrypy
from sqlalchemy import create_engine, text
from jinja2 import Environment, FileSystemLoader
from whoosh.index import create_in
#from whoosh.query import *
from whoosh.qparser import QueryParser

os.chdir(os.path.dirname(os.path.realpath(__file__)))
import search_engine as se



# -------------------------------------------------------------------------------------------------------------------- #
#                                               DATABASE AND JINJA2 SETUP                                              #
# -------------------------------------------------------------------------------------------------------------------- #
db_engine = create_engine("sqlite:///:memory:", encoding = "utf-8")
#db_engine = create_engine("mysql://user:password@localhost/foo", encoding = "utf-8") #https://docs.sqlalchemy.org/en/14/core/engines.html

env = Environment(loader = FileSystemLoader(os.path.join("content", "html")))



# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
class Root(object):
	def get_darkmode(self):
		if "darkmode" in cherrypy.request.cookie and cherrypy.request.cookie["darkmode"].value in (1, "1", "true"):
			return {"int": 1, "str": "dark", "checked": "checked"}
		else:
			return {"int": 0, "str": "", "checked": ""}
	
	def render_page(self, path, **kwargs):
		template = env.get_template(path)
		return template.render(darkmode = self.get_darkmode(), **kwargs)
	
	def lookup(self, q):
		print("Query detected:", q)
		with se.index.searcher() as searcher:
			QueryParser(q, se.schema)
			pass
		return ""

	@cherrypy.expose
	def livesearch(self):
		q = cherrypy.request.body.read().decode()
		if q == "":
			return ""
		return self.lookup(q)

	@cherrypy.expose
	def search(self, q = ""):
		if q == "":
			print("Empty Search Query")
			raise cherrypy.HTTPRedirect("/")
			#return ""
		print("Returning webpage...")
		return self.render_page("sites/search.html", results = self.lookup(q))
	
	@cherrypy.expose
	def index(self):
		return self.render_page("sites/index.html")
	
	@cherrypy.expose
	def view(self):
		with db_engine.connect() as conn:
			result = conn.execute(text("select * from recipe"))
			print(result.all())
		return self.render_page("sites/view.html")

cherrypy.quickstart(Root(), config = "app.config")
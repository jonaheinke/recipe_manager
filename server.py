import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    DATABASE SETUP                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
import sqlite3
#from sqlalchemy import create_engine, text
#db_engine = create_engine("sqlite:///:memory:", encoding = "utf-8")
#db_engine = create_engine("mysql://user:password@192.168.178.43/database", encoding = "utf-8") #https://docs.sqlalchemy.org/en/14/core/engines.html

def execute_query(q):
	try:
		connection = sqlite3.connect(os.path.join("database", "database.db"), 5)
	except sqlite3.Error as e:
		print(e)
		return False, None

	cursor = connection.cursor()
	result = None
	try:
		if isinstance(q, str):
			cursor.execute(q)
			result = cursor.fetchall()
		elif isinstance(q, list) or isinstance(q, tuple) or isinstance(q, set):
			result = []
			for el in q:
				cursor.execute(el)
				result.append(cursor.fetchall())
	finally:
		connection.commit()
		connection.close()
	return result



# -------------------------------------------------------------------------------------------------------------------- #
#                                                    INDEXING SETUP                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from whoosh.fields import Schema, KEYWORD, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.analysis import StandardAnalyzer, StemmingAnalyzer, NgramFilter, NgramAnalyzer
#from whoosh.query import *
from whoosh.qparser import QueryParser

search_schema = Schema(id = STORED, title = TEXT, ingredients = KEYWORD, content = TEXT(StemmingAnalyzer())) #https://whoosh.readthedocs.io/en/latest/quickstart.html
search_path = "search"
ALWAYS_REBUILD = False

if ALWAYS_REBUILD:
	search_index = create_in(search_path, search_schema)
elif os.path.exists(search_path):
	search_index = open_dir(search_path)
else:
	pass

def rewrite_search_index(documents):
	writer = search_index.writer()
	for document in documents:
		writer.add_document(**document)
	writer.commit()

def add_document_to_index(document):
	writer = search_index.writer()
	writer.add_document(document)
	writer.commit()

def search(self, q):
	with search_index.searcher() as searcher:
		result = searcher.search(q)
	return result



# -------------------------------------------------------------------------------------------------------------------- #
#                                                     JINJA2 SETUP                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
from jinja2 import Environment, FileSystemLoader
from jac import CompressorExtension
from html_minify import HTMLCompressor

env = Environment(extensions = [CompressorExtension], loader = FileSystemLoader("content"))
#env.compressor_classes = {"text/html": HTMLCompressor}
env.compressor_output_dir = "./content/min"
env.compressor_static_prefix = "/min"
env.compressor_source_dirs = "./content"



# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
import cherrypy

rewrite_search_index([
	{"id": 0, "content": "cool stuff"},
	{"id": 1, "content": "my favorite cookies"},
	{"id": 2, "content": "nice drink"}
])
qp = QueryParser("content", search_schema)

with search_index.searcher() as searcher:
	#print(searcher.search(qp.parse("cookies"))[0])
	pass

class Website(object):
	# --------------------------------------------------- INDEXING --------------------------------------------------- #
	def lookup(self, q):
		print("Query detected:", q)
		result = {}
		with search_index.searcher() as searcher:
			query = QueryParser(q, search_schema)
			result = searcher.search(query)
			pass
		return result

	# --------------------------------------------------- RENDERING -------------------------------------------------- #
	def get_darkmode(self):
		if "darkmode" in cherrypy.request.cookie:
			if cherrypy.request.cookie["darkmode"].value in (0, "0", "false"):
				return {"str": "light", "checked": ""}
			return {"str": "dark", "checked": "checked"}
		return {"str": "", "checked": ""}
	
	def render_page(self, path, **kwargs):
		return env.get_template(path).render(darkmode = self.get_darkmode(), **kwargs)
	
	@cherrypy.expose
	def modify(self):
		q = cherrypy.request.body.read().decode()
		if q == "":
			raise cherrypy.HTTPRedirect("/")
		return "This is an unfinished site."

	@cherrypy.expose
	def livesearch(self):
		q = cherrypy.request.body.read().decode()
		if q == "":
			return ""
		return self.lookup(q)

	@cherrypy.expose
	def search(self, q = ""):
		if q == "":
			raise cherrypy.HTTPRedirect("/")
		return self.render_page("html/search.html", results = self.lookup(q))
	
	@cherrypy.expose
	def view(self, id):
		if id == "":
			raise cherrypy.HTTPRedirect("/")
		'''
		with db_engine.connect() as conn:
			result = conn.execute(text("select * from recipe"))
			print(result.all())
		
		cursor = connection.cursor()
		result = None
		try:
			cursor.execute("select * from recipe where recipeid = " + id)
			result = cursor.fetchall()
		finally:
			return result
		'''
		if int(id) not in []:
			raise cherrypy.HTTPRedirect("/")
		return self.render_page("html/view.html")
	
	"""
	@cherrypy.expose
	def css(self, file, file2 = ""):
		print("#"*30)
		print(file, file2)
		return self.render_page("css/" + file + ("/" + file2 if file2 else ""))
		#return self.render_page("html/sites/index.html")
	
	@cherrypy.expose
	def js(self, file = ""):
		
		return self.render_page("html/sites/index.html")
	"""

	@cherrypy.expose
	def index(self):
		print(cherrypy.request.body.headers)
		return self.render_page("html/index.html")

cherrypy.quickstart(Website(), config = "app.config")
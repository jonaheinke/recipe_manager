import os, sqlite3, cherrypy
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import search_engine

# -------------------------------------------------------------------------------------------------------------------- #
#                                                    DATABASE SETUP                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
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
#                                                     JINJA2 SETUP                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
from jinja2 import Environment, FileSystemLoader
from jac import CompressorExtension
from html_minify import HTMLCompressor

env = Environment(extensions = [CompressorExtension], loader = FileSystemLoader("content"), autoescape = True)
#env.compressor_classes = {"text/html": HTMLCompressor}
env.compressor_output_dir = "./content/min"
env.compressor_static_prefix = "min"
env.compressor_source_dirs = "./content"



# -------------------------------------------------------------------------------------------------------------------- #
#                                                     EXIT FUNCTION                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
"""
def on_exit():
	print("nice")

signalhandler = cherrypy.process.plugins.SignalHandler(cherrypy.engine)
for signal in ["SIGTERM", "SIGHUP", "SIGQUIT", "SIGINT"]:
	signalhandler.handlers[signal] = on_exit
signalhandler.subscribe()
"""



# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
class Website(object):
	# ------------------------------------------------- MODIFICATION ------------------------------------------------- #
	@cherrypy.expose
	def modify(self):
		q = cherrypy.request.body.read().decode()
		if q == "":
			raise cherrypy.HTTPRedirect("/")
		return "This is an unfinished site."

	# --------------------------------------------------- RENDERING -------------------------------------------------- #
	def get_darkmode(self):
		if "darkmode" in cherrypy.request.cookie:
			if cherrypy.request.cookie["darkmode"].value in (0, "0", "false"):
				return {"str": "light", "checked": ""}
			return {"str": "dark", "checked": "checked"}
		return {"str": "", "checked": ""}
	
	def render_page(self, path, **kwargs):
		return env.get_template(path).render(darkmode = self.get_darkmode(), **kwargs)

	# ----------------------------------------------------- PAGES ---------------------------------------------------- #
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def livesearch(self):
		return search_engine.search(cherrypy.request.body.read().decode())
	
	@cherrypy.expose
	def view(self, id):
		if id == "":
			raise cherrypy.HTTPRedirect("/")
		"""
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
		"""
		"""
		if int(id) not in []:
			raise cherrypy.HTTPRedirect("/")
		"""
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
		#print(cherrypy.request.body.headers)
		return self.render_page("html/index.html")

cherrypy.quickstart(Website(), config = "app.config")
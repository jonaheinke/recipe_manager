import os, time, threading
from whoosh.fields import Schema, KEYWORD, NGRAMWORDS, NUMERIC, TEXT
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser, MultifieldParser, FieldsPlugin, FieldAliasPlugin
#from whoosh.analysis import StandardAnalyzer, StemmingAnalyzer, NgramFilter, NgramAnalyzer
#from whoosh.query import *

#https://whoosh.readthedocs.io/en/latest/quickstart.html
schema = Schema(
	id = NUMERIC(stored = True, unique = True, signed = False),
	category = TEXT,
	title = NGRAMWORDS(2, 20, True, 2.0),
	ingredients = KEYWORD,
	content = NGRAMWORDS(4, 20))

#TODO: Synonyme https://whoosh.readthedocs.io/en/latest/api/lang/wordnet.html
search_path = "search"
ALWAYS_REBUILD = False
min_search_length = 2

if not os.path.exists(search_path):
	os.mkdir(search_path)

def rebuild_index():
	index = create_in(search_path, schema)
	writer = index.writer()
	writer.add_document(id = 0, title = "Test Words", content = "super nice")
	writer.add_document(id = 1, title = "Apple Banana Cucumber")
	writer.add_document(id = 2, title = "Deck Elevator Floor", category = "test")
	writer.add_document(id = 3, title = "Pen Pineapple Apple Pen")
	writer.add_document(id = 4, title = "wordsalad")
	writer.add_document(id = 5, title = "injection")
	writer.commit()
	return index

if __name__ == "__main__":
	rebuild_index()
else:
	if ALWAYS_REBUILD:
		index = rebuild_index()
	else:
		index = open_dir(search_path)
	
	#TODO: Doesnt work. Only triggers once.
	#timer = threading.Timer(86400, index.optimize)
	#timer.daemon = True
	#timer.start()

	writer = AsyncWriter(index, 0.5)

	parser = MultifieldParser(["content", "title"], schema, {"content": 1.0, "title": 2.0})
	#parser.add_plugin(SingleQuotePlugin())
	parser.remove_plugin_class(FieldsPlugin) #https://whoosh.readthedocs.io/en/latest/api/qparser.html#plug-ins

	def search(q):
		if len(q) < min_search_length:
			return []
		result = []
		with index.searcher() as searcher:
			search_result = searcher.search(parser.parse(q))
			#result = list(map(lambda x: x.fields(), search_result))
			result = [item.fields() for item in search_result]
		return result
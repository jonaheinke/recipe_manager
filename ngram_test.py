from whoosh.fields import Schema, TEXT, STORED, NGRAMWORDS
from whoosh.index import create_in, open_dir
from whoosh.analysis import StandardAnalyzer, StemmingAnalyzer, NgramFilter, NgramAnalyzer, NgramWordAnalyzer
#from whoosh.query import *
from whoosh.qparser import QueryParser, MultifieldParser, FieldsPlugin

analyzer = NgramAnalyzer(3)
schema = Schema(
	id = STORED,
	category = TEXT(field_boost = 3.0),
	#title = TEXT(analyzer, False)
	title = NGRAMWORDS(2, 20, False, 2.0)
)

index = create_in("search", schema)
#index = open_dir("search")

writer = index.writer()
writer.add_document(id = 0, title = "Test Words")
writer.add_document(id = 1, title = "Apple Banana Cucumber")
writer.add_document(id = 2, title = "Deck Elevator Floor", category = "test")
writer.add_document(id = 3, title = "Pen Pineapple Apple Pen")
writer.commit()



#parser = QueryParser("title", schema)
parser = MultifieldParser(["category", "title"], schema, {"category": 3.0, "title": 2.0})
parser.remove_plugin_class(FieldsPlugin)

with index.searcher() as searcher:
	result = searcher.search(parser.parse("Test"))
	print(str(len(result)) + " results")
	for f in result:
		print(f["id"])
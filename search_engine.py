import os
from whoosh.fields import Schema, KEYWORD, TEXT, STORED
from whoosh.index import create_in, open_dir

schema = Schema(id = STORED, title = TEXT, ingredients = KEYWORD, content = TEXT) #https://whoosh.readthedocs.io/en/latest/quickstart.html

class RecipeIndex():
	ALWAYS_REBUILD = True

	def __init__(self, path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "search")): #open or create index
		if not self.ALWAYS_REBUILD and os.path.exists(path):
			self.index = open_dir(path)
		else:
			self.index = create_in(path, schema)

	def rewrite_search_index(self):
		writer = self.index.writer()
		for i in range(3):
			writer.add_document()
		writer.commit()
	
	def add_document_to_index(self):
		writer = self.index.writer()
		writer.add_document()
		writer.commit()
	
	def search(self, q):
		with self.index.searcher() as searcher:
			result = searcher.search(q)
		return result

if __name__ == "__main__":
    pass
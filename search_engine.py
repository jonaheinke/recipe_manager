import os
from whoosh.fields import Schema, KEYWORD, TEXT, STORED
from whoosh.index import create_in

schema = Schema(id = STORED, title = TEXT, ingredients = KEYWORD, content = TEXT) #https://whoosh.readthedocs.io/en/latest/quickstart.html
index = create_in(os.path.join(os.path.dirname(os.path.realpath(__file__)), "content", "search"), schema)

def rewrite_search_index():
	writer = index.writer()
	writer.add_document()
	writer.commit()

if __name__ == "__main__":
    pass
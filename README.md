# recipe_manager
## Description
TBD

## Goals
- creating a simple, local recipe book directed at domestic use
- light on data traffic (when using mobile data if you have set a VPN up to your home network)
- no annoying trackers and ads
- simple HTML, CSS and JS without unnecessary code or wrapper elements

Currently the home page consumes 5.3kB of data before browser cacheing and html/css minification.

## Setup
```shell
$ pip install CherryPy SQLAlchemy Jinja2 Whoosh
# insert recipe data into database
$ python search_engine.py
$ python server.py
```
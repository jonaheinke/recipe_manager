# personal website for managing recipes

[![license](https://img.shields.io/github/license/jonaheinke/recipe_manager)](LICENSE)
[![last commit](https://img.shields.io/github/last-commit/jonaheinke/recipe_manager)](https://github.com/jonaheinke/recipe_manager/commit)
[![open issues](https://img.shields.io/github/issues/jonaheinke/recipe_manager)](https://github.com/jonaheinke/recipe_manager/issues)
[![code size](https://img.shields.io/github/languages/code-size/jonaheinke/recipe_manager)](#)

## Description

**TODO**

## Goals

- creating a simple, local recipe book directed at domestic use
- simple import from other recipe websites
- light on data traffic (when using mobile data)
- no annoying trackers and ads
- simple HTML, CSS and JS without unnecessary code or wrapper elements
- can be hosted locally or on a cheap/free server

## Navigating the repo

Recommendation: install the [Sass](https://marketplace.visualstudio.com/items?itemName=Syler.sass-indented) and [Sass Live Compiler](https://marketplace.visualstudio.com/items?itemName=glenn2223.live-sass) extensions for VS Code

- `index.html` is the main page, you should study this first
- if you want to study the recipe database, look into **TODO**
- if you want to study the search index, look into **TODO**

## Installation

### Requirements for webserver

- PHP 7.1 or newer
- MySQL
- PDO extension for PHP
- SQLite Extension for PHP
- mbstring xtension for PHP
- .htaccess enabled with rewrite engine

### Setup

1. git clone to local folder
2. (not recommended) for newest TNTSearch version: run `composer update` in the project root
3. run `composer install` in the project root
4. copy local folder contents to the root of the webserver
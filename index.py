# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, json, g, redirect, request, abort
from hashids import Hashids
import random
import os
import countsyl
import click
from pprint import pprint
app = Flask(__name__)
hashids = Hashids()

SYL_1="5"
SYL_2="8"
SYL_3="5"
BOOK_META="books/books.json"

with app.open_resource(BOOK_META) as f:
	books = json.load(f)

@app.before_request
def before_request():
	g.books = books

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', books=g.books["books"]), 404

@app.route("/")
def index():
	return render_template('index.html', books=g.books["books"])

@app.route("/<id>")
def get_poem(id):
	if id.isdigit():
		book = get_book_by_id(int(id))
		if book:
			return generate_poem(book[0])
		else:
			return render_template('book_not_found.html', books=g.books["books"])
	else:
		abort(404)

@app.route("/<id>/<code>")
def display_poem(id, code):
	if id.isdigit():
		book = get_book_by_id(int(id))
		poem = read_poem_code(book[0],code)
		return render_template('display_poem.html', poem=poem, book=book[0], books=g.books["books"])
	else:
		abort(404)

def get_book_by_id(id):
	book = [book for book in g.books["books"] if book["id"] == id]
	return book

def generate_poem(book):
	fname = 'books/'+book["file"]+'.json'
	if os.path.isfile(fname):
		with open(fname, 'r') as f:
			b = json.load(f)
			code_list =	[
				random.randrange(0,len(b[SYL_1])), 
				random.randrange(0,len(b[SYL_2])), 
				random.randrange(0,len(b[SYL_3]))
				]
			#code = "_".join(map(str,code_list))
			code = hashids.encode(code_list[0], code_list[1], code_list[2])
			#encode
			return redirect(url_for('display_poem', id=book["id"], code=code))
	else:
		abort(404)

def read_poem_code(book, code):
	#decode
	#code_list = code.split("_")
	code_list = hashids.decode(code)
	code_list = map(int, code_list)
	if book:
		with open('books/'+book["file"]+'.json', 'r') as f:
			b = json.load(f)
			try:
				poem = [
					b[SYL_1][code_list[0]],
					b[SYL_2][code_list[1]],
					b[SYL_3][code_list[2]]
				]
			except IndexError:
				abort(404)

			return poem
	else:
		return render_template('book_not_found.html', books=g.books["books"])

@app.cli.command('register')
@click.option('--file', prompt=True)
@click.option('--title', prompt=True)
@click.option('--author', prompt=True)
@click.option('--year', prompt=True)
@click.option('--image', prompt=True)
def register_book(file,title,author,year,image):
	#read the file provided, create a json file, update the books.json meta file
	new_book = dict()

	with app.open_resource(BOOK_META) as f:
		books = json.load(f)

	book = get_book_details(file)

	if books["books"]:
		new_id = books["books"][-1]["id"] + 1
	else:
		new_id = 1
	new_book["id"] = new_id
	new_book["title"] = title
	new_book["file"] = file
	new_book["author"] = author
	new_book["image"] = image
	new_book["year"] = year

	books["books"].append(new_book)
	with open('books/books.json', 'w') as f:
		json.dump(books,f)
	output = (title, new_id)
	click.echo("%s Registered\nID: %d" % output)

def get_book_details(filename):
	with open('books/'+filename, 'r') as f:
		book = dict()
		for line in f:
			line = clean_line(line)
			if len(line):
				syl_count = countsyl.count_syllables(line)
				#book[syl_count[0]].append(line)
				book.setdefault(syl_count[0],[]).append(line)
		
		with open('books/'+filename+'.json', 'w+') as f:
			json.dump(book,f)

	return book

def clean_line(line):
	bad_character_pairs = [
		['"','"'],['“','”'],['‘','’'],["'","'"]
	]
	cleanline = line.strip().rstrip(',')
	cleanline = cleanline[:1].upper() + cleanline[1:] #capitalize the first letter
	for char_pair in bad_character_pairs:
		if not cleanline.startswith(char_pair[0]):
			cleanline = cleanline.rstrip(char_pair[1]) 
			#remove the last character, if there is not a matching pair at the front

	return cleanline

if __name__ == "__main__":
	app.run(debug=True)
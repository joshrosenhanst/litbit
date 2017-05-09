# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, json
import random
import os
import countsyl
app = Flask(__name__)

def get_books():
	book_list = []
	books = os.listdir("books")
	for book in books:
		book = unicode(book.replace(".txt", ""), 'utf-8')
		book_list.append(book)

	return book_list

def read_book(filename):
	f = open("books/"+filename, "r")
	return get_haiku(f)

def get_haiku(book):
	print "get haiku"
	five_syllables = []
	seven_syllables = []
	grab_bag = []

	for line in book:
		syllable = random.randint(1,10)
		clean_line = line.strip().rstrip(',')
		clean_line = clean_line[:1].upper() + clean_line[1:]
		if not clean_line.startswith('"'):
			clean_line = clean_line.rstrip('"')

		if not clean_line.startswith('“'):
			clean_line = clean_line.rstrip('”')

		if not clean_line.startswith('‘'):
			clean_line = clean_line.rstrip('’')

		if not clean_line.startswith("'"):
			clean_line = clean_line.rstrip("'")

		if len(clean_line):
			syl_count = countsyl.count_syllables(clean_line)

			#if syl_count[0] >= 4 and syl_count[0] <= 7:
			#	grab_bag.append(clean_line)
			if syl_count[0] == 5 and syl_count[1] in [5,6]:
				five_syllables.append(clean_line)

			if syl_count[0] == 7 and syl_count[1] in [7,8]:
				seven_syllables.append(clean_line)

	if len(five_syllables) > 2 and len(seven_syllables) > 0:
		return [random.choice(five_syllables), random.choice(seven_syllables), random.choice(five_syllables)]
	else:
		return False

	#if len(grab_bag) > 2:
	#	return [random.choice(grab_bag), random.choice(grab_bag), random.choice(grab_bag)]
	#else:
	#	return False


@app.route("/", methods=['GET', 'POST'])
def layout():
	books = get_books()
	if request.method == 'POST':
		title = request.form["book"]
	else:
		title = "Moby Dick"

	haiku = read_book(title+".txt")
	line1 = unicode(haiku[0], 'utf-8')
	line2 = unicode(haiku[1], 'utf-8')
	line3 = unicode(haiku[2], 'utf-8')
	return render_template('layout.html', title=title,line1=line1,line2=line2,line3=line3,books=books)

if __name__ == "__main__":
	app.run()
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import random
import countsyl
app = Flask(__name__)

def read_book(filename):
	f = open("books/"+filename, "r")
	return get_haiku(f)

def get_haiku(book):
	print "get haiku"
	five_syllables = []
	seven_syllables = []

	for line in book:
		clean_line = line.strip().rstrip(',').capitalize()
		if not clean_line.startswith('“'):
			clean_line = clean_line.rstrip('”')

		if len(clean_line):
			syl_count = countsyl.count_syllables(clean_line)
			if syl_count[0] == 5 and syl_count[1] in [5,6]:
				five_syllables.append(clean_line)

			if syl_count[0] == 7 and syl_count[1] in [7,8]:
				seven_syllables.append(clean_line)

	if len(five_syllables) > 2 and len(seven_syllables) > 0:
		return [random.choice(five_syllables), random.choice(seven_syllables), random.choice(five_syllables)]
	else:
		return False


@app.route("/")
def layout():
	title = "Moby Dick"
	haiku = read_book("moby.txt")
	line1 = unicode(haiku[0], 'utf-8')
	line2 = unicode(haiku[1], 'utf-8')
	line3 = unicode(haiku[2], 'utf-8')
	return render_template('layout.html', title=title,line1=line1,line2=line2,line3=line3)

if __name__ == "__main__":
	app.run()
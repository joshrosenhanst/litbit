# Lit Bit - Auto Generated Poems
LitBit generates a small poem from lines popular literature.

### Tech
* Python 2.7
* Flask
* Uwsgi

### Dev Environment Setup
1. Clone repo
1. `apt-get install python-dev python-pip`
1. `pip install virtualenv`
1. `virtualenv litbit`
1. `source litbit/bin/activate`
1. `pip install uwsgi flask hashids`
1. `flask run`
1. Useful info: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04

### Adding books
1. Grab free use books from Project Gutenberg or similar source in .txt format. 
1. Remove all unnecessary text from before or after the book text (ex: table of contents, prefaces, etc)
1. Add the .txt file to the books/ directory
1. Grab a cover image, as well as title, author, and year details.
1. Run the `flask register` command to add new books to the books.json list
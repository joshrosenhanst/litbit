# Lit Bit - Auto Generated Poems
LitBit generates a small poem from lines popular literature.

### Tech
* Python 2.7
* Flask
* Uwsgi

### Usage
1. `source litbit/bin/activate`
1. Make a copy of litbit.ini.sample and name it litbit.ini. Update the file as necessary.
1. Grab free use books from Project Gutenberg or similar source. Remove all unnecessary text from before or after the book text (ex: table of contents, prefaces, etc)
1. Run the `flask register` command to add new books to the books.json list
1. Run `uwsgi --ini litbit.ini` to run the app
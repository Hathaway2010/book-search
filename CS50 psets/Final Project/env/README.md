# YOUR PROJECT TITLE
#### Description:

This simple book search enables a hypothetical bookstore to transform a CSV, TSV, or comparable spreadsheet document containing books' titles, authors, and prices into a SQLite database and sets up a website using Python, Flask, HTML, and CSS via which users may search the database.

I developed this on my computer rather than in the CS50 IDE, so some files involved in testing my project (a Python program that queries the database and prints the full inventory and a Python program that deletes the table in the database) are not included, nor the files involved in setting up Flask in my virtual environment. To gain experience, I researched and used the sqlite3 library itself rather than the CS50 library.

##### import.py

The file import.py is the means by which a bookstore can import its data, which must be formatted as a CSV, TSV, or other file in which text values are separated by special characters. At present, import.py is a command-line program; I may eventually build a GUI for it, using (perhaps) tkinter. It requires a single command-line argument in addition to the program name: the name of the CSV (or other) file to import. It then prompts the user for information about the provided spreadsheet: the name of the title field, of the author field, and of the price field, as well as the format of the author field (whether the name is formatted as `First_name Last_name` or `Last_name, First_name`) and the delimiter and quote character in the spreadsheet. From here, import.py creates or connects to a database named inventory.db, in which it creates a table called inv. It then reads the spreadsheet file row-by-row into inv, making a few alterations:

1. It parses the author into last name and first name or, if applicable, two last names (more on this later; it required a separate function whose implementation was complex)
2. It keeps the initial author string and title string to display (if necessary) in results.
3. It makes sure the price is formatted with two decimal points and at least one digit before the decimal point.

I considered creating a password-protected webpage to which bookstore staff could upload the spreadsheet, allowing them to configure the database in a more user-friendly way; however, this struck me as an unnecessary security risk, since I envisioned this being used from a central computer. As I mentioned above, I still might want to investigate creating a GUI for this for a bookstore computer.

Meanwhile, parsing the author names proved to be a significant challenge, and the solutions I reached were necessarily imperfect. Initially, I planned to leave the author field as a single string containing both first and last names; however, this proved problematic for searching in ways I will discuss, so I decided to split author names into first and last name. I initially envisioned this app as a solution for the bookstore where I used to work, and with whose data entry practices I am quite familiar, and in the end I decided to import these names as if the file I were given would follow the data entry practices of this bookstore:

1. I would assume that any book with more than two authors was given an author name of *various* or no author name
2. I would assume that any book with two authors would separate those authors with an ampersand (*&*) and supply only their last names, so that everything before the ampersand would be considered the first author's last name and everything after would be considered a second author's last name.
3. I would read name parts like *von*, *van*, and *de* as part of the last name
4. I would assume that name parts like *Mc* or *Mac* would be separated from the rest of the last name by a space
5. I would assume that middle names would not be included in the data

I could also have assumed (6) that names would be supplied in the format `Last_name, First_name`, as our bookstore does, with the separating comma, and that is easily the preferable format, since the program need not guess where the first name stops and the last name begins. In the event data is provided in that format, I simply split the name on the comma. The only instance of a comma in a name I could think of was in suffixes like *Jr.* and *Sr.*, so I removed those suffixes from the fields that would be searched. I then assumed that, if splitting the author field on the comma produced more than a single list item, that the first list item would be a last name and the second list item would be a first name, disregarding anything after that.

However, I did, hesitantly, attempt to provide an option that would parse names supplied in the format `First_name Last_name` as well. Ideally, I think, a program would make use of lists of first and last names to make educated guesses about where to separate a name like "Mary Alice van der Meer" (which would still be imperfect, as we can see from *Catch-22*'s Major Major Major Major), or perhaps match names against an approved list of authors' first and last names; however, I chose the simpler practice of:

1. eliminating common suffixes
2. arbitrarily putting any single-word name in the last name field
3. putting the first word of a two-word name in the first name field and the last word in the last name field
4. splitting names containing *de*, *van*, and so forth at that word, including it in the last name and putting everything else in the first name
5. and if all of the above fails, putting the first word in the first name field and the last word (suffixes having been eliminated) in the last name field.

Step 5 is obviously suboptimal (Mary Alice is in a rough place), but perhaps better than other options.

Formatting author and title strings was another challenge. My bookstore's data is entered automatically in all caps. One might imagine that others' could be entered in other ways. So I wanted to achieve standard title case. In order to do this, I imported a library called titlecase, designed to implement title case more intelligently than Python's native string method (which capitalizes all words, even, say, articles, and any letter that comes after a punctuation mark, such as the *t* in *can't*). Unfortunately, it was a little too smart for me: I had entered some of my data in all caps and some not, and when a single field contained both forms of capitalization the function kept the all-caps text capitalized, "assuming" the capitals were used for emphasis. I decided this form of data entry (changing from all caps to not in the same field) would be unlikely enough in the wild that this function was superior (since some books contain acronyms in their titles, and it would be good to preserve capitalization in such cases).

The titlecase library is available here: https://github.com/ppannuto/python-titlecase  It is offered under the MIT license (https://github.com/ppannuto/python-titlecase/blob/main/LICENSE.md).

##### application.py

The file application.py is, as in the examples provided for the course, the central file for my Flask app, which has only one route, "/," with a GET method and a POST method. The GET method serves a search page; the POST method serves a results page after calling search.py on any information entered on the search page.

##### search.py

Implementing a search function was a challenge, and could be refined significantly (I would especially like to add spell checking, so that common misspellings of an author's name would still bring up that author, e.g., so that "Stephanie Meyers" would bring up "Stephenie Meyer" ). I implement my search by running a series of queries on the SQLite database, using Python's sqlite3 library.

I decided that I would not separate author and title searches, though at some point I may add the ability to do searches for just one or the other; I may also attempt to add an ISBN search feature, but this would be challenging for data from my bookstore because only used paperbacks are entered with real ISBNs instead of system-generated but superficially valid false SBNs there; I would need access to some kind of listing or database of books and their ISBNs.

When a user enters one or more search terms, search.py will first search case-insensitively for exact matches, then for matches of decreasing sizes of groups of words from the search terms. If a given search term (word or words) is longer than four characters, it will also search the fields that *contain* that term, using wildcards. Shorter search terms, unfortunately, turn up too many irrelevant results. For example, searching for "On Writers & Writing" would bring up "The 10% Solution" because the letters "on" are in "solution."

However, this made searches for some authors' last names a problem when the author name field was a single field. For instance, a user looking for Celeste Ng should be able to search for "Ng" instead of "Celeste Ng" or "Ng, Celeste" and get accurate results (without getting every -ing title in the database); to enable such exact matches is reason I separated author names into first and last names.

Finally, I payed close attention to the order in which results are returned: the more exact a match, the closer to the top it should appear. I might, in addition, want eventually to implement a popularity feature, in which each time a result is clicked, the likelier it will be to show up higher in otherwise equally ranked search results.

##### CSV and TSV files

I used these to check my work. I do not have a file from the bookstore where I used to work, but I do have three self-created files, as well as a library file from a different local organization.

##### Templates

In my templates folder, layout.html sets the basic form of an HTML document and links to my stylesheet. The search bar and submit button themselves are in index.html (along with a commented-out dropdown menu with which a user can choose between author and title search, which I may use eventually). In results.html, I used Jinja to interpolate the results of the search function, passed in in application.py. The commented-out sections here represent other fields that I might eventually display in my results table.

##### Static

The static files folder contains a single, simple CSS file that formats the search page and results somewhat more attractively. I decided to fly without Bootstrap to get design practice.

##### Testing

I was unable to acquire a CSV file I can use to test this app from the bookstore for which it was (in theory) designed. I have used self-created csv files and 20210105acquisitions.csv, a local nonprofit's library records; since their data entry conventions are somewhat different, I have not perfectly conformed my program to those conventions, but I made a few adjustments to attempt to account for the fact that, for instance, some of their authors are comma-separated and some are not, and I made the price field optional, because this organization lends rather than sells these books, and learned that my search is still fast with more than 2000 entries. Since the target bookstore's inventory consists of almost 200,000 books, this doesn't tell me that much, but it is encouraging. Oddly, when I attempt to load this large CSV file in the CS50 IDE, it fails to load, apparently because some character was not encoded in a way that could be read, but it works fine on my computer.

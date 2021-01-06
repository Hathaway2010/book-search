from sys import argv, exit
import csv
import sqlite3
from titlecase import titlecase

def main():
    if len(argv) != 2:
        print("Usage: python import.py filename.csv")
        exit(1)
    author = input("Author field name: ")
    while True:
        format = input("""Format: 'first last' or 'last first' (with or without commas)?
                      Type '1' for the first option or '2' for the second:  """)
        if format in ["1", "2"]:
            break;
    title = input("Title field name: ")
    price_exists = input("Is there a price field? y/n:")
    if price_exists == "y":
        price = input("Price field name: ")
    separator = input("Delimiter in provided file (~ or , or \\t, e.g.): ")
    quote = input("Quote character in provided file (\" or \' or |, e.g.): ")
    # this code from https://docs.python.org/3/library/sqlite3.html
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS inv")
    c.execute("CREATE TABLE inv (id INTEGER PRIMARY KEY, title TEXT, author TEXT, author_first TEXT, author_last TEXT, author2_last TEXT, price TEXT)")
    with open(argv[1], "r", newline="") as file:
        reader = csv.DictReader(file, delimiter=separator, quotechar=quote)
        for row in reader:
            author_parse(format, author, row)
            if price_exists == "y" and row[price]:
                fl = float(row[price])
                row[price] = "{0:.2f}".format(fl)
                data = {"title": titlecase(row[title]), "author": titlecase(row[author]), "author_first": row['author_first'], "author_last": row['author_last'], "author2_last": row["author2_last"], "price": row[price]}
            else:
                data = {"title": titlecase(row[title]), "author": titlecase(row[author]), "author_first": row['author_first'], "author_last": row['author_last'], "author2_last": row["author2_last"], "price": "0.00"}
            c.execute("REPLACE INTO inv (title, author, author_first, author_last, author2_last, price) VALUES (:title, :author, :author_first, :author_last, :author2_last, :price)",
            data)

    conn.commit()
# mutates reader_row to contain author_first an author_last key-value pairs,
# used in the next step
def author_parse(firstlast, author_field, reader_row):
    reader_row["author_first"] = None
    reader_row["author_last"] = None
    reader_row["author2_last"] = None
    if firstlast == "1":
        # this function found at https://www.kite.com/python/answers/how-to-remove-a-comma-from-a-string-in-python#:~:text=Use%20str.,'%20in%20str%20with%20''%20.
        # get rid of any comma separating a Jr. or Sr.; first-name last-name Format
        # probably won't have a comma separating names
        author_string = reader_row[author_field].replace(",", "")
        author_names = author_string.split()
        if len(author_names) == 1:
            if author_names[0].lower() != "various":
                reader_row["author_last"] = author_names[0]
                return
        if len(author_names) == 2:
            reader_row["author_first"] = author_names[0]
            reader_row["author_last"] = author_names[1]
            return
        if len(author_names) > 2:
            for word in author_names:
                if word.lower() in ["sr.", "jr.", "iii"]:
                    del author_names[author_names.index(word)]
                    print(author_names)
            if "&" in author_names:
                reader_row["author_last"] = " ".join(author_names[: author_names.index("&")])
                reader_row["author2_last"] = " ".join(author_names[author_names.index("&") + 1:])
                return
            for word in author_names:
                if word.lower() in ["von", "van", "de", "des", "mc", "mac"] and author_names.index(word) != 0:
                    reader_row["author_first"] = " ".join(author_names[: author_names.index(word)])
                    reader_row["author_last"] = " ".join(author_names[author_names.index(word):])
                    return
                else:
                    reader_row["author_first"] = author_names[0]
                    reader_row["author_last"] = author_names[-1]
                    return
    else:
        auth = reader_row[author_field]
        if "&" in auth:
            reader_row["author_last"] = auth[:auth.index("&")].strip()
            reader_row["author2_last"] = auth[auth.index("&") + 1:].strip()
            return
        if "," in auth:
            author_names = auth.split(",")
            for word in author_names:
                if word.lower() in ["sr.", "jr.", "iii"]:
                    del author_names[author_names.index(word)]
            if len(author_names) == 1:
                reader_row["author_last"] = author_names[0]
                return
            if len(author_names) > 1:
                reader_row["author_last"] = author_names[0]
                reader_row["author_first"] = author_names[1]
                return
        else:
            author_names = auth.split()
            if len(author_names) == 1:
                reader_row["author_last"] = author_names[0]
                return
            if len(author_names) == 2:
                reader_row["author_last"] = author_names[0]
                reader_row["author_first"] = author_names[1]
                return
            for word in author_names:
                if word.lower() in ["sr.", "jr.", "iii"]:
                    reader_row["author_last"] = author_names[:author_names.index(word)]
                    reader_row["author_first"] = author_names[author_names.index(word) + 1:]
                    return
            if len(author_names) > 2:
                reader_row["author_last"] = author_names[0]
                reader_row["author_first"] = author_names[-1]
                return



# regarding titlecase: Python's built-in title case function is not intelligent enough for this
# so, poking around on Stack Overflow (in particular, here:
# https://stackoverflow.com/questions/1549641/how-can-i-capitalize-the-first-letter-of-each-word-in-a-string)
# I found this library: https://github.com/ppannuto/python-titlecase under the
# MIT license





main()

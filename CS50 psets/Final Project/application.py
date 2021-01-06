from flask import Flask, render_template, request

import "search.py"

app = Flask(__name__)

@app.route("/", methods="['GET', 'POST']")
def index():
    if request.method == "POST":
        # something like: results = search(request.form.get("book_search"))
        return render_template("results.html", results=results)
    else:
        return render_template("index.html")

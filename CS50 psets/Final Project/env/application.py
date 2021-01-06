from flask import Flask, render_template, request


from search import search


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        results = search(request.form.get("book_search").split())
        print(results)
        return render_template("results.html", results=results, length=len(results))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()

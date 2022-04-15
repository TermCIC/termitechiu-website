from flask import Flask, redirect, url_for, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutus")
def drchiu():
    return render_template("aboutus.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/publications")
def publications():
    return render_template("publications.html")

if __name__ == "__main__":
    app.run()

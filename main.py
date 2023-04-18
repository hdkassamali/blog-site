from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

n_point = "https://api.npoint.io/5872c7375bbfdbf38c76"
response = requests.get(n_point)
posts = response.json()


@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact-me")
def contact_me():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for post in posts:
        if post["id"] == index:
            requested_post = post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
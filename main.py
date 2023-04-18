from flask import Flask, render_template, url_for, request
import requests
import smtplib
import os
gmail_user = os.environ.get("gmail_user")
gmail_pass = os.environ.get("gmail_pass")

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

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(gmail_user, gmail_pass)
        connection.sendmail(gmail_user, gmail_user, email_message)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for post in posts:
        if post["id"] == index:
            requested_post = post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
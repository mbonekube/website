from flask import Flask, render_template
from datetime import date
import requests
import smtplib
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


MY_EMAIL = "egabtech@yahoo.com"
YAHOO_APP_PASSWORD = "kbpvztnpzmcuzpmq"     # This is not my yahoo password, it's a password generated to work with
TO_EMAIL = "egabtek@gmail.com"              # third-party apps.


posts = requests.get("https://api.npoint.io/44634e270da855b41a53").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Contact(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    phone = StringField("Phone Number(Optional)")
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('SEND')


@app.route('/')
def get_all_posts():
    current_year = date.today().year
    return render_template("index.html", all_posts=posts, year=current_year)


@app.route("/post/<int:index>")
def show_post(index):
    current_year = date.today().year
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post, year=current_year)


@app.route('/about')
def about():
    current_year = date.today().year
    return render_template("about.html", year=current_year)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    current_year = date.today().year
    # if request.method == "POST":
    #     data = request.form
    #     send_email(data["name"], data["email"], data["phone"], data["message"])
    #     return render_template("contact.html", msg_sent=True, year=current_year)
    # return render_template("contact.html", msg_sent=False, year=current_year)
    form = Contact()
    if form.validate_on_submit():
        send_email(form.name.data, form.email.data, form.phone.data, form.message.data)
        return render_template("contact.html", msg_sent=True, year=current_year, form=form)
    return render_template("contact.html", msg_sent=False, year=current_year, form=form)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message From Your Blog\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, YAHOO_APP_PASSWORD)
        connection.sendmail(MY_EMAIL, TO_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

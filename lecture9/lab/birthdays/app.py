import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        # Get data from HTML
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Insert new line into database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);", name, month, day)

        # Display newly entered name in list
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays;")
        return render_template("index.html", birthdays=birthdays)


# Route to delete a person/birthday
@app.route("/delete", methods=["POST"])
def delete():

    # Get id of person to be removed
    removed_row = request.form.get('id')

    # Delete that person from the database
    db.execute("DELETE FROM birthdays WHERE id = (?);", removed_row)

    # dispay updated list by redirecting to / just like when we update with a new name
    return redirect("/")

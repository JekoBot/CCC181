"""UniformQ: a queue app for claiming PE uniforms in the university.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

SERVICES = [
    {"id": 1, "name": "PE shirt"},
    {"id": 2, "name": "PE pants"},
]

# Sample data for the demo. A real app would load this from a database later.
# Each ticket: number, name, student_id, size, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana", "student_id": "2024-0001", "size": "M",
     "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Ben", "student_id": "2024-0002", "size": "L",
     "service_id": 2, "status": "waiting"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/join")
def join_form():
    return "Join form coming soon"


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
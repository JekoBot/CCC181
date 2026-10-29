"""UniformQ: a queue app for claiming PE uniforms in the university.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

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
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    numbers = [t["number"] for t in TICKETS]
    return render_template("index.html", name="Ana", tickets=numbers)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
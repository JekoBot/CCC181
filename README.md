# UniformQ

UniformQ is a queue management app for claiming PE uniforms at the MSU-IIT Langkit University Shop. Students join the queue from their phone with their name, class section and up to two items with sizes, then see their queue number, status and how many people are ahead of them. Staff use a dashboard to see the waiting list in order, call the next student, and mark them served or no-show. It is built with Flask, Jinja and Bootstrap for CCC181.

## How to run

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

On macOS or Linux, activate with `source .venv/bin/activate`. Then open http://127.0.0.1:5000.

## Pages

- `/join`: join the queue
- `/queue/<number>`: My place, which refreshes itself every 10 seconds
- `/staff`: staff dashboard

## Notes

- The staff dashboard has no login yet, so anyone who opens `/staff` can use it.
- Tickets are kept in a Python list, so they reset every time the app restarts. A database comes in Week 4.
- Documentation for Week 3 (personas, requirements, wireframes, self-review, accessibility check, usability test and report) is in `docs/week3/`.
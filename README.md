# UniformQ

UniformQ is a queue management app for claiming PE uniforms at the MSU-IIT Langkit University Shop. Students join the queue from their phone with their name, class section and up to two items with sizes, then see their queue number, status and how many people are ahead of them. Staff use a dashboard to see the waiting list in order, call the next student, and mark them served or no-show. Tickets are stored in PostgreSQL, so none are lost when the server restarts. It is built with Flask, SQLAlchemy and Bootstrap for CCC181.

## How to run

You need Python 3.11 or newer and Docker Desktop.

```
git clone https://github.com/JekoBot/CCC181.git
cd CCC181
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace `change-me` with your own password, in both lines. Then:

```
docker compose up -d
flask --app app db upgrade
flask --app app seed
flask --app app run --debug
```

On macOS or Linux, activate with `source .venv/bin/activate` and copy the file with `cp .env.example .env`. Then open http://127.0.0.1:5000.

`docker compose down` stops the database and keeps the data. `docker compose down -v` also deletes the data.

## Pages

- `/join`: join the queue
- `/queue/<number>`: My place, which refreshes itself every 10 seconds
- `/staff`: staff dashboard
- `/staff/items`: manage items

## Notes

- The staff pages have no login yet, so anyone who opens `/staff` can use them. Login comes in Week 11.
- Each browser can hold one active ticket. A different browser or cleared cookies can still join again.
- `.env` holds the database password and is not committed. `.env.example` shows the variables the app needs.

## Documentation

- [Requirements](docs/requirements.md)
- Week 3: [personas](docs/week3/personas.md), [accessibility check](docs/week3/accessibility.md), [report](docs/week3/report.md)
- Week 4: [schema and ERD](docs/week4/schema.md), [validation](docs/week4/validation.md), [persistence](docs/week4/persistence.md), [report](docs/week4/report.md)
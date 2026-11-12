# Validation in three layers

The same rules are checked in three places. The browser gives users fast feedback, Flask is the real gatekeeper, and the database is the last line of defense if there is a bug.

## Layer 1: Browser

The join form uses `required` on Name, Class Section, Item 1 and Size 1, and `maxlength` to match the column lengths. Item 2 and Size 2 are optional.

| Rule | How I tested it | What happened |
| --- | --- | --- |
| Name is at most 80 characters | Typed 100 characters in the Name field | The field stopped at 80 |
| Class section is at most 30 characters | Typed 100 characters in the Class Section field | The field stopped at 30 |

Anyone can skip these checks, which is why the next two layers exist.

## Layer 2: Flask (skipping the form with curl)

Tickets before the requests: 2. Tickets after: 2.

| Rule | How I tested it | What happened |
| --- | --- | --- |
| Name, section, item and size are checked | `curl.exe` with an empty name and section, `item1=999` and `size1=XXL` | 400, nothing saved |
| Name length limit | `curl.exe` with a 200-character name | 400, nothing saved |
| Item 2 must differ from Item 1 | `curl.exe` with `item1=1` and `item2=1` | 400, nothing saved |
| Size 2 needs an item 2 | `curl.exe` with `size2=L` and no `item2` | 400, nothing saved |

## Layer 3: Database (skipping Flask with psql)

| Rule | Constraint type | How I tested it | PostgreSQL error |
| --- | --- | --- | --- |
| An item must exist | FOREIGN KEY | `INSERT INTO ticket_items` with `item_id` 999 | `ERROR: insert or update on table "ticket_items" violates foreign key constraint "ticket_items_item_id_fkey"` |
| Size must be real | CHECK | size `'XXL'` | `ERROR: new row for relation "ticket_items" violates check constraint "ck_ticket_items_size"` |
| Only two item positions | CHECK | position `3` | `ERROR: new row for relation "ticket_items" violates check constraint "ck_ticket_items_position"` |
| Status must be known | CHECK | `UPDATE tickets SET status = 'lost'` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Name must not be blank | CHECK | name of three spaces | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_name_not_blank"` |
| Name is required | NOT NULL | name `NULL` | `ERROR: null value in column "name" of relation "tickets" violates not-null constraint` |
| Item names are unique | UNIQUE | a second `'PE shirt'` | `ERROR: duplicate key value violates unique constraint "items_name_key"` |
| One active ticket per session | UNIQUE (partial index) | a second `waiting` ticket with the same `session_id` | `ERROR: duplicate key value violates unique constraint "one_active_ticket_per_session"` |
| The same item cannot be on a ticket twice | UNIQUE | item 1 at position 2 on a ticket that already has item 1 | `ERROR: duplicate key value violates unique constraint "uq_ticket_items_ticket_item"` |
| One item per position | UNIQUE | item 2 at position 1 on a ticket that already has position 1 | `ERROR: duplicate key value violates unique constraint "uq_ticket_items_ticket_position"` |
| An item with tickets cannot be deleted | RESTRICT | `DELETE FROM items WHERE id = 1;` | `ERROR: update or delete on table "items" violates foreign key constraint "ticket_items_item_id_fkey" on table "ticket_items"` |

Every constraint type in the schema is covered: FOREIGN KEY, CHECK, NOT NULL, UNIQUE and RESTRICT.

The failed inserts used up some ticket ids, so the next real queue number skips them. `GENERATED ALWAYS AS IDENTITY` never reuses a number, which is what NFR-02 needs.

## No SQL in f-strings
**git grep -nE “f[”’].(SELECT|INSERT|UPDATE|DELETE)” -- “.py”**

This printed nothing. All queries use SQLAlchemy (`db.select`, `update`, `db.session.add` and `db.session.delete`), which sends values separately from the SQL, so user input cannot become code.
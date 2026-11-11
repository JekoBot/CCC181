# UniformQ database schema

## 2a. Nouns in the requirements

| Req ID | Requirement | Nouns | Table or column? |
| --- | --- | --- | --- |
| FR-01 | A **student** can join the **queue** with their **name**, **section**, **items** and **sizes**. | student, queue, name, section, item, size | `tickets`, not a table, `tickets.name`, `tickets.section`, `items`, `ticket_items.size` |
| FR-02 | A student can see their **queue number**, **status**, and how many people are **ahead** of them. | queue number, status, ahead | `tickets.id`, `tickets.status`, computed |
| FR-04 | A staff member can see the waiting list in queue order, with each student's name, section, items and sizes. | waiting list, name, section, items, sizes | computed queue, `tickets`, `ticket_items` |
| FR-05 | A staff member can call the next student, mark them served, or mark them no-show. | staff member, student, status | `tickets.status` |
| FR-07 | A student can leave the queue. | student, queue, status | `tickets.status` |
| FR-08 | A staff member can switch an item off. | staff member, item, active state | `items.active` |

The queue is not a table: it is every ticket with status `waiting`. The number of people ahead is computed, not stored.

## 2b. Tables and columns

| Table | Columns |
| --- | --- |
| `items` | `id`, `name`, `active` |
| `tickets` | `id`, `name`, `section`, `status`, `joined_at`, `session_id`, `called_at` |
| `ticket_items` | `id`, `ticket_id`, `item_id`, `size`, `position` |

## 2c. Column types and constraints

| Table | Column | PostgreSQL type | Constraint | Why |
| --- | --- | --- | --- | --- |
| `items` | `id` | `integer GENERATED ALWAYS AS IDENTITY` | PRIMARY KEY | Gives every uniform item a stable identifier. |
| `items` | `name` | `varchar(60)` | NOT NULL UNIQUE | Prevents duplicate item names. |
| `items` | `active` | `boolean` | NOT NULL DEFAULT `true` | Lets staff stop offering an item without deleting it, so old tickets keep their item names. |
| `tickets` | `id` | `integer GENERATED ALWAYS AS IDENTITY` | PRIMARY KEY | The queue number. The database assigns it, so it is never reused and two students never share one. It is also unique and always in join order, so it decides who is ahead. |
| `tickets` | `name` | `varchar(80)` | NOT NULL, CHECK (length(trim(name)) > 0) | A ticket must have a student name, not blank spaces. |
| `tickets` | `section` | `varchar(30)` | NOT NULL, CHECK (length(trim(section)) > 0) | Staff match the ticket to the student's receipt by section. |
| `tickets` | `status` | `varchar(20)` | NOT NULL DEFAULT `'waiting'`, CHECK (status IN (`'waiting'`, `'called'`, `'served'`, `'no-show'`, `'left'`)) | Allows only known queue states. |
| `tickets` | `joined_at` | `timestamptz` | NOT NULL DEFAULT `now()` | Records when the student joined, for the time shown to staff and for reports. |
| `tickets` | `session_id` | `varchar(64)` | NOT NULL | A random token kept in the student's browser session, used to stop one browser holding two active tickets. |
| `tickets` | `called_at` | `timestamptz` | NULL | Records when staff called the student, so the wait before being called can be measured. |
| `ticket_items` | `id` | `integer GENERATED ALWAYS AS IDENTITY` | PRIMARY KEY | Identifies each item line on a ticket. |
| `ticket_items` | `ticket_id` | `integer` | NOT NULL, FOREIGN KEY REFERENCES `tickets(id)` ON DELETE CASCADE | Connects each item line to its ticket; a mistaken ticket can be deleted together with its items. |
| `ticket_items` | `item_id` | `integer` | NOT NULL, FOREIGN KEY REFERENCES `items(id)` ON DELETE RESTRICT | Prevents an item line from pointing to a missing item, and keeps old tickets readable. |
| `ticket_items` | `size` | `varchar(3)` | NOT NULL, CHECK (size IN (`'XS'`, `'S'`, `'M'`, `'L'`, `'XL'`, `'2XL'`)) | Allows only real uniform sizes. |
| `ticket_items` | `position` | `smallint` | NOT NULL, CHECK (position IN (1, 2)), UNIQUE (`ticket_id`, `position`) | Limits a ticket to two items. |
| `ticket_items` | `ticket_id`, `item_id` | | UNIQUE (`ticket_id`, `item_id`) | The same item cannot appear twice on one ticket. |

Every constraint type is used: PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE and CHECK, and `joined_at` is a `timestamptz`. Nothing that can be computed is stored: the number of people ahead is counted from `status` and `id`.

## 2d. ERD

![ERD](./erd.png)

One ticket has one or two ticket items. One item appears in many ticket items. Each ticket item belongs to exactly one ticket and one item.

| Foreign key | On parent delete | Reason |
| --- | --- | --- |
| `ticket_items.ticket_id` → `tickets.id` | `CASCADE` | A ticket's item lines have no meaning without the ticket, so deleting a mistaken ticket removes them too. |
| `ticket_items.item_id` → `items.id` | `RESTRICT` | Do not delete an item while old tickets still refer to it. Switch it off with `items.active` instead. |

## 2e. Indexes

```sql
-- One active ticket per browser session: a second waiting or called ticket is refused.
CREATE UNIQUE INDEX one_active_ticket_per_session
ON tickets (session_id)
WHERE status IN ('waiting', 'called');

-- "Call next" and the waiting list read only waiting tickets, oldest first.
CREATE INDEX ix_tickets_waiting
ON tickets (joined_at)
WHERE status = 'waiting';
```

## 2f. Normalization check

1. **One value per cell (1NF):** Yes. Each column holds one value. Items are not stored as a list such as `"PE shirt, PE pants"`; each item is its own row in `ticket_items`.
2. **Depends on the whole key (2NF):** Yes. In `ticket_items`, `size` and `position` describe one specific item on one specific ticket, so they depend on the whole row.
3. **No hidden copies (3NF):** Yes. Every non-key column in `tickets` describes that one ticket, and no column depends on another non-key column. An item's name and active state are stored only in `items`. A student's name and section are stored on the ticket because students have no accounts, so each ticket records who joined for that claim. If students later get accounts or a student ID, I would move name and section into a `students` table.

## 2g. Rules kept in the app

- **People ahead** are the waiting tickets with a smaller `id`. The id is unique and always in join order, so two students who join at the same instant are never counted as ahead of each other. "Call next" picks the oldest waiting ticket by `joined_at`, with `id` as the tiebreaker.
- **Ticket items** are inserted in the same transaction as the ticket, starting at position 1, and a join with no items is rejected.
- **Status changes** follow fixed transitions: `waiting` → `called`; `called` → `served` or `no-show`; `waiting` or `called` → `left`. Each update names the expected current status in its WHERE clause, so an invalid change updates zero rows.
- **Switched-off items** are hidden from the join form, and a join that includes one is rejected like an item that does not exist. Staff pages still list every item.
- **Called_at** called_at is set when staff press Call next, using now() in the database.

## Duplicate tickets

A student who leaves, or who is served or marked as a no-show, can join again and gets a new ticket with a new queue number. The old ticket stays as a row, so reports such as "how many left before being served" still work.

When a student joins, the app generates a random `session_id`, saves it in their browser session, and stores it on the ticket. While that ticket is `waiting` or `called`, opening the join page sends them back to My place. If two submits from the same browser arrive together, the unique index refuses the second ticket, and the app rolls back and sends the student to their existing ticket.

This only controls one browser, because students have no accounts. A different browser or cleared cookies could still join twice. This is a known limit.

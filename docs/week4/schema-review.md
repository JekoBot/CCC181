# Schema Self-Review

I reviewed the UniformQ tables (`items`, `tickets`, `ticket_items`) against the requirements. These are the problems I found.

## Switching an Item Off

### Works Well
`ticket_items.item_id` uses `RESTRICT`, so an item that has been referenced by tickets cannot be deleted accidentally. This ensures historical tickets remain readable.

### Problem
The same rule prevents staff from stopping an item from being offered when it is no longer available, such as when a size run is out of stock. They cannot delete the item, and leaving it visible allows students to join the queue for something that cannot be handed out. The schema documentation says to "switch it off instead," but the `items` table had no column to support this.

### Change
Added:

```sql
active BOOLEAN NOT NULL DEFAULT TRUE
```

The default value populates existing rows automatically. The join form displays only active items, and any join request containing an inactive item is rejected in the same way as a request for a non-existent item. Staff pages continue to show all items so historical tickets retain their item names.

---

## Position in Line

### Works Well
There is no stored position-in-line column. The number of people ahead is calculated dynamically from ticket status and `joined_at`.

### Problem
Two students who join at the same instant may receive identical `joined_at` values, causing each to be counted as ahead of the other.

### Change
People ahead are now counted using `id`, which is unique and generated in join order. The `joined_at` field remains for displaying join times and producing reports.

The "Call Next" operation selects the oldest waiting ticket using:

1. `joined_at`
2. `id` as a tiebreaker

A partial index was also added because this is the application's most common query:

```sql
CREATE INDEX idx_tickets_waiting_joined_at
ON tickets (joined_at)
WHERE status = 'waiting';
```

---

## Duplicate Tickets

### Works Well
When a student leaves or is served, a new ticket is created for future visits while the old ticket remains available for reporting. This preserves useful information such as how many students left before being served.

### Problem
The "one active ticket" rule existed only in application code. Two rapid submissions from the same browser could pass validation before either request completed, creating duplicate active tickets.

### Change
Added:

```sql
session_id TEXT
```

A partial unique index now enforces one active ticket per browser session:

```sql
CREATE UNIQUE INDEX uq_active_session
ON tickets (session_id)
WHERE status IN ('waiting', 'called');
```

The database now rejects a second active ticket from the same browser session.

This still applies only to a single browser because students do not have accounts. Users can still join multiple times using a different browser or after clearing cookies. This remains a known limitation.

---

## Two Items per Ticket

### Works Well
The existing constraints:

```sql
CHECK (position IN (1, 2))
UNIQUE (ticket_id, position)
UNIQUE (ticket_id, item_id)
```

limit each ticket to two item selections and prevent the same item from being selected twice.

### Problem
Nothing guarantees that a ticket contains at least one item, and a ticket could theoretically contain only position `2`.

### Change
The application now:

- Inserts the ticket and item rows within a single transaction.
- Always starts item numbering at position `1`.
- Rejects join requests with no selected items.

A database trigger was not added because the transaction logic already guarantees the required behavior, and a trigger would increase maintenance complexity.

---

## Statuses

### Works Well
A `CHECK` constraint limits `status` to five valid values. Keeping `left` separate from `no-show` allows reporting to distinguish between students who voluntarily left and students who failed to return when called.

### Problem
The `CHECK` constraint only validates allowed values. It does not prevent invalid transitions, such as changing a ticket from `served` back to `waiting`.

### Change
Status changes are enforced through application logic with fixed transitions:

- `waiting → called`
- `called → served`
- `called → no-show`
- `waiting → left`
- `called → left`

Each update query includes the expected current status in its `WHERE` clause. Invalid transitions therefore update zero rows.

This rule remains in the application rather than the database because, for the scale of this project, application-level enforcement is sufficient and simpler to maintain than database triggers.
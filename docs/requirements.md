# Requirements

# UniformQ requirements

**Setting:** Claiming PE uniforms at the MSU-IIT Langkit University Shop on claiming days
**People who wait:** Students who ordered a PE uniform, such as Ana Ramos in [docs/week3/personas.md](week3/personas.md)
**People who serve:** The student assistant who hands out uniforms, such as Rey Mendoza in [docs/week3/personas.md](week3/personas.md)

**Problem statement:** A student who needs to claim a PE uniform needs a way to see how many people are ahead of them and when their turn is near, because the shop has no queue, only a sizing receipt that shows what was ordered but not who arrived first, so students stand in the sun for over an hour.

Never reuse or renumber an ID. A requirement that is dropped stays in the table, marked *Dropped*.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue with their name, section, items and sizes. | Must | **Yes** | Built (Week 3) |
| FR-02 | A student can see their queue number, status and how many people are ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-03 | The app rejects incomplete or invalid forms with a clear message. | Must | **Yes** | Built (Week 3) |
| FR-04 | A staff member can see the waiting list in queue order, with each student's name, section, items and sizes. | Must | **Yes** | Built (Week 3) |
| FR-05 | A staff member can call the next student, mark them served, or mark them no-show. | Must | **Yes** | Built (Week 3) |
| FR-06 | A student's status updates without refreshing the page. | Must | No | Built (Week 3) |
| FR-07 | A student can leave the queue. | Must | **Yes** | Built (Week 3) |
| FR-08 | A staff member can switch an item off, so students can no longer choose it. | Should | **Yes** | Built |
| FR-09 ★ | My place reminds the student to bring their receipt to the counter. | Should | No | Built (Week 3) |
| FR-10 ★ | A student who is already waiting or called is sent back to My place and cannot hold a second active ticket in the same browser. | Should | **Yes** | Built |
| FR-11 ★ | A staff member can serve or mark no-show only a student who has been called, so the queue order cannot be skipped. | Must | **Yes** | Built (Week 3) |
| FR-12 | A staff member can see how many students are waiting and when each one joined. | Should | **Yes** | Built |
| FR-13 | A staff member can see how many students left before being served, per day. | Could | **Yes** | Later |
| FR-14 | A staff member can delete a mistaken ticket. | Should | **Yes** | Built |
| FR-15 | Only staff can open the staff pages. | Should | **Yes** | Later (Week 11) |
| FR-16 | The app will tell when to go to the venue | Should | No | Built Built |


★ marks requirements specific to this setting: the receipt reminder (FR-09), one active ticket per student (FR-10) and serving only called students (FR-11).

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two students never get the same queue number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | Only valid statuses, sizes and items can be stored, even if someone skips the form. | Data integrity | Must |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |
| NFR-06 | A student can join the queue in under 30 seconds. | Usability | Should |
| NFR-07 | My place loads in under 2 seconds on slow mobile data. | Performance | Should |

## MVP

**MVP:** FR-01 to FR-07 and FR-11, plus NFR-01, NFR-02, NFR-03 and NFR-05. This is the smallest version that fixes the problem: a student gets a queue number, sees how many people are ahead, and staff serve students in order, with no ticket lost on restart.

**Out of scope this semester:**

- **Push notifications or SMS** when a student's turn is near. Students see their status on My place instead, because sending messages needs an outside service.
- **Taking payment in the app.** Staff check the student's receipt at the counter, as they do now.
- **Student accounts or student ID login.** Students join with a name and section only, so the one-active-ticket rule (FR-10) only works for one browser.

## Check with a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Student claiming a uniform |	“I need to know when to go, not just a count.” | Kept FR-02, and My place now shows “almost your turn, make your way to the venue” and “go to the counter” states. |
| | | |
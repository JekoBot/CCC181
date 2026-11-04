# Self-review

Reviewed against Ana Ramos (student waiting) and Rey Mendoza (staff member). Each screen was checked on both the phone and the laptop frame.

## Join queue

**Can my persona tell what to do on this screen within 5 seconds?**
Mostly. On the laptop, "Join the queue" is visible as the card title, the labels are plain, and "Get your Queue Number" is the obvious last step. On the phone the card has no title, so Ana has only the UniformQ logo to tell her where she is.

**Is the queue number or status always visible where the person needs it?**
Not applicable yet. Ana does not have a queue number until she submits the form, and her status appears on My place afterwards.

**Do the words match what people in my setting actually say?**
Yes. "Class Section", "Item 1" and "Size 1" match the sizing form students already filled in, and "Queue Number" is used consistently with My place.

**Is the action the staff member does most often the easiest one to reach?**
This is a student screen, so the frequent action is joining the queue. "Get your Queue Number" is the biggest control and is easy to reach. The "Join as Staff" link is very small and sits next to the logo, where a student could tap it by mistake and staff could miss it.

**Does the phone version still show the most important thing first?**
Partly. The form starts at the top, but without a heading, and the dropdowns for items and sizes are small for Ana, who is standing and holding her phone with one hand.

**Which "Because ..., my interface must ..." rules does this screen follow, and which does it break?**
It follows Ana's rule 3 (works on a phone, light and quick to load). It only partly follows rule 4 (bring her receipt), because the reminder is on My place but the Join screen doesn't tell her to copy the items and sizes from her receipt. There is also no error state drawn for FR-03.

**Works well:** The labels use the words students already know from the sizing form, and the single button says what the student gets. This supports match with the real world.
**Problem:** Students could pick different items or sizes from what is on their receipt. The phone frame also lacks a page title, which is a recognition rather than recall issue.
**Change:** Add a line under the title: "Choose the items and sizes on your receipt." Add a "Join the queue" title to the phone frame, and make "Join as Staff" a clearly labeled link away from the logo.

## My place

**Can my persona tell what to do on this screen within 5 seconds?**
Yes. The queue number is the largest thing on the screen, followed by the status, the place in the queue and the items, so Ana can see where she stands at a glance.

**Is the queue number or status always visible where the person needs it?**
Partly. The status and place are visible without scrolling, but the status is a plain text box that looks the same as the other fields which is important because that is what Ana should check changes for.

**Do the words match what people in my setting actually say?**
Yes. "Your queue number", "Status", "Place in queue", "Leave queue" and "Please bring your Receipt to the Counter when called" use plain words from the shop.

**Is the action the staff member does most often the easiest one to reach?**
Staff actions do not belong on this screen. Ana's one action, Leave queue, is a large button and easy to reach.

**Does the phone version still show the most important thing first?**
Mostly. The queue number comes first. "3 people ahead of you" wraps onto two lines in a small box, even though it is the other thing Ana wants to see first.

**Which "Because ..., my interface must ..." rules does this screen follow, and which does it break?**
It follows rule 1 (Big Queue number at the top) and rule 4 (receipt reminder). It only partly follows rule 1 for the people ahead, which is smaller text.

**Works well:** The queue number is the largest element, and the receipt reminder sits on the same screen, so Ana knows what to bring when she is called. This supports visibility of system status.
**Problem:** The status looks like an ordinary field so Ana could miss that her turn has come. The receipt reminder is small and at the bottom. 
**Change:** Show the status as a badge, make the people-ahead line larger and keep it on one line. Move the receipt reminder next to the status.

## Staff dashboard

**Can my persona tell what to do on this screen within 5 seconds?**
Yes. "Call next" is the largest control, with "2 people waiting" inside it, and the table lists the students in order underneath.

**Is the queue number or status always visible where the person needs it?**
Yes for waiting students, each row has a status. No for the student who has just been called: nothing shows who Rey is currently serving, so he could lose track of the person he is about to hand a uniform to.

**Do the words match what people in my setting actually say?**
Mostly. "Call next", "Serve" and "No-show" are plain. The flow note says "Mark served" while the button says "Serve".

**Is the action the staff member does most often the easiest one to reach?**
Yes. Call next is the largest button, at the top, and separate from the row actions. The laptop table also has a Call button on every row, which gives Rey two ways to do the same job, and the phone table has no row Call at all.

**Does the phone version still show the most important thing first?**
Yes. Call next comes before the table. The phone table is more cramped than the laptop one, with Name and Items squeezed together.

**Which "Because ..., my interface must ..." rules does this screen follow, and which does it break?**
It follows rule 1 (single queue order), rule 2 (waiting count) and rule 3 (compact table, plain labels). It breaks rule 4: neither frame has a Section column, even though Rey needs name, section, items and sizes.

**Works well:** Call next is large, shows how many are waiting, and sits above the list, so the most frequent action is the easiest to reach. This supports recognition rather than recall.
**Problem:** The table has no Section, so Rey cannot match a student to their receipt. There is no "now serving" display, and two different ways to call a student. These are match with the real world, visibility of system status and consistency issues.
**Change:** Add a Section column on the laptop and show it under the name on the phone. Add a "Now serving: #14 Ana" bar above the table. Keep Call next and remove the per-row Call.
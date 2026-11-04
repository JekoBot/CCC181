## Ana Ramos, the student waiting to claim a PE uniform

> "I wondered why the location wasn't properly arranged from the beginning so we wouldn't have to stand under the sun for so long." (interview)

| | |
| --- | --- |
| **Photo or sketch** | ![Sketch of Ana](./screenshots/persona_ana.png) |
| **Age, role and background** | 18 , 1st year BS Computer Science student at MSU-IIT. She was sized for her PE uniform earlier, filling in her name, size, section and payment on a form that doubles as her receipt. She finds out when and where to claim from the Langkit University Shop's Facebook announcements (interview). |
| **Goals** | 1. Claim her PE uniform without losing most of an afternoon to waiting.<br>2. Know roughly when her turn is near, so she can do other things instead of standing in line the whole time (interview).<br>3. Not have to scrutinize the details of her schedule to check if she has the free time to wait in line. |
| **Frustrations** | 1. She waited more than an hour in line, with nothing to do but chat with a friend (interview).<br>2. She couldn't tell how many people were ahead of her because the line was long (interview).<br>3. She stood under the hot sun for over an hour before the line was moved to the air-conditioned theater room (interview). |
| **Devices and context** | On her android phone using mobile data that is either slow or almost gone. She waits standing in line, with friends nearby (interview). |
| **Tech comfort** | High. She uses various apps that improve comfort such as delivery and taxi apps, she also uses Facebook to follow campus announcements (interview). |
| **Accessibility needs** | reading a phone screen in bright sun, one hand free while standing, slow mobile data. |

### Scenario

Ana sees the Langkit University Shop's Facebook post saying PE uniforms can be claimed this week. She already has her receipt from the sizing. She goes to the shop and finds a long line outside in the sun. Nothing tells her how many people are ahead, so she stays put and chats with a friend for over an hour. Only then does the line move into the air-conditioned theater room. With the app, she would join the queue from her phone, choose her items and sizes according to the receipt she has, and wait somewhere cool. She sees her number and how many people are ahead, and when her turn is near the app tells her to come to the counter with her receipt.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue with my name, section, items and sizes | Join | FR-01 |
| Check my number and how many people are ahead | My place | FR-02 |
| See when my turn is near, without refreshing | My place | FR-06 |
| Leave the queue if I can't make it | My place | FR-07 |

### What this means for my interface

1. Because Ana couldn't tell how many people were ahead of her (interview), my interface must show her ticket number and the people ahead as the biggest things on My place.
2. Because she wanted to do other things while waiting (interview), my interface must show a clear status such as "Called" that updates by itself, so she doesn't have to stay in line.
3. Because she finds out about claiming through Facebook on her phone (interview), my interface must work on a phone, load fast, and be reachable from a link she can open straight from the post.
4. Because staff ask students to show their receipt when they claim (staff interview), my interface must remind her on My place to bring her receipt to the counter.

---

## Rey Mendoza, the staff member handing out PE uniforms

> "People will cut in line, and I found the venue we used to be overcrowded." (interview)

| | |
| --- | --- |
| **Photo or sketch** | ![Sketch of Rey](./screenshots/persona_rey.png) |
| **Age, role and background** | 20 years old, student assistant at the Langkit University Shop who helps hand out PE uniforms on claiming days. Students are first sized on a form with their name, size, section and payment, and that form works as their receipt. Students show it when they claim, and staff work from these receipts and laptop spreadsheet records (interview). No tickets or queue numbers were given out. |
| **Goals** | 1. Keep the line orderly so people can't cut in front of others (interview).<br>2. Keep the claiming area from getting overcrowded (interview).<br>3. Hand out uniforms quickly without misplacing order receipts or giving the wrong size (interview). |
| **Frustrations** | 1. People cut in line (interview).<br>2. The venue they used was overcrowded (interview).<br>3. The receipt shows a student's name, size, section and payment, but not who arrived first, so nothing records who is next (interview). |
| **Devices and context** | Used a laptop running a spreadsheet application (such as Google Sheets or Excel) during the claiming process (interview). Works standing over a table while students wait in line. |
| **Tech comfort** | Medium. Comfortable using basic laptop software and spreadsheets, but any new tool must make lookup quick so it doesn't slow down the physical line. |
| **Accessibility needs** | High visual contrast for quick scanning on a laptop screen, keyboard shortcuts to reduce mouse use, and large, clear text that is readable while standing over a table. |

### Scenario

On a claiming day, students arrive holding the receipt from their sizing. There are no queue numbers, so they line up on their own, and the venue fills up quickly. Some students push in front of others, and Rey has no record of who really came first. He keeps his laptop open to a spreadsheet of sized students, finds each name, checks the receipt, and hands over the right size, trying not to misplace receipts or give the wrong one. With the app, students join the queue from their phones and wait elsewhere, so the venue stays emptier. Rey opens the dashboard in his laptop's browser, sees the next student in order with their name, section, items and sizes, taps "Call next", checks the receipt, hands over the uniform, and marks the student as served.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting list in one clear queue order, with each student's name, section, items and sizes | Staff dashboard | FR-04 |
| Call the next student | Staff dashboard | FR-05 |
| Mark a student as served | Staff dashboard | FR-05 |
| Mark a student as no-show (optional, one tap) | Staff dashboard | FR-05 |

### What this means for my interface

1. Because people cut in line and nothing records who came first (interview), my interface must show every student in a single queue order that staff cannot rearrange, so the list settles any argument.
2. Because the venue was overcrowded (interview), my interface must show how many students are waiting, so staff can see the line without anyone crowding the area.
3. Because Rey works from a laptop spreadsheet and needs quick lookup (interview), my interface must show the queue as one compact table with the next student at the top, so a lookup takes seconds.
4. Because he must not give the wrong size or misplace a receipt (interview), my interface must show each student's name, section, items and sizes next to their queue number, so he can compare the information to the receipt.
5. Because he stands over a table scanning a laptop screen (interview), my interface must use high contrast and large text, and let him use Call next, Served and No-show with the keyboard (Tab and Enter) as well as the mouse.
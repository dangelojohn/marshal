# Surface 6 — Driver SMS

**Role:** Driver / carrier · **Job:** be told where and when, confirm with one word · **Status:** designed (D-005 §4), not built · **Device:** any phone, plain SMS — no app, no login, ever

**Source docs:** `01_product/14_surface_map.md` §"Customer — SMS + portal"

---

## Why this surface looks the way it does

**The driver will never log in. Full stop.** They're in a truck, possibly mid-route, and the entire interaction budget is reading one text and replying with one word. This is deliberately the smallest surface in the whole system — not a scaled-down app, not a lightweight web view, **plain SMS**, because anything requiring a tap-through link or an install is a surface this person won't use.

Free-text replies are parsed by an LLM into structured intent, with a keyword fallback when the model is unreachable (D-009) — so the design constraint isn't just "short message," it's **"a message a human can reply to in their own words, that the system can still parse reliably."** That shapes the message copy itself as much as any visual layout: the prompt below is really a copy-design exercise (what does the text say, exactly) dressed as a UI mockup (a phone showing the Messages app), because there is no other UI to design.

This isn't a Stitch "app screen" in the way the other six surfaces are — there's no interface to build, only a conversation to design well. Use Stitch here to mock up the **Messages app thread itself** (a realistic iOS/Android SMS conversation view), which is the only artifact worth generating — it lets you read the exchange the way the driver actually will, and catch anything that reads wrong in that context before it ships as a Twilio template.

### Design brief

**Color** — none, by design. This should render as a stock Messages app (iMessage blue bubbles for outbound/system, grey for inbound/driver replies), because inventing a custom SMS visual identity would misrepresent what this surface actually is. The "design" lives entirely in the copy.

**Type** — system default (SF Pro on iOS, Roboto on Android) — again, deliberately not a Marshal-branded typeface, because the driver's phone renders this, not Marshal.

**Layout / signature element**: the message copy itself is the whole deliverable. Three message types to get right:
```
1. ASSIGNMENT           2. CONFIRMATION          3. REMINDER/CHANGE
Marshal: Dock 4          Driver: Y                Marshal: Dock 4 now
at 14:20 for PR-1041.                              14:35 (was 14:20).
Reply Y to confirm.       Marshal: Confirmed.       Reply Y to confirm.
                          See you at 14:20.
```

Keep every outbound message under ~160 characters (one SMS segment), always end with an explicit, single-word reply instruction, and always confirm receipt of a reply in the next message — silence after a reply is exactly the "did it register?" failure the runner watch's confirmation screen (surface 2) was designed to avoid, and the same principle applies here even without a screen.

---

## The Stitch prompt

```
Design a mobile phone screen showing a realistic SMS/Messages app conversation
thread between an automated logistics system called "Marshal" and a truck
driver delivering freight to a trade show loading dock. Render this as a
standard iOS Messages app UI — NOT a custom-branded interface. Use the real
iMessage visual convention: outbound/system messages in blue rounded bubbles
aligned right... actually, reverse this: the SYSTEM message should appear as
an incoming business/automated text, so render it in light grey bubbles
aligned LEFT (as a business SMS sender would appear to the driver), and the
DRIVER's replies in blue bubbles aligned RIGHT, matching how a real recipient's
Messages app looks when texting with an automated/business number. Standard
system font (SF Pro), standard iOS status bar and Messages app chrome
(contact name at top, e.g. "MARSHAL" or "55055"-style short code), timestamps
in small grey text between message groups.

DO NOT invent a custom color scheme, custom bubble shapes, custom iconography,
or any Marshal-specific branding within the chat itself — the entire point of
this design is that it looks exactly like an ordinary text message thread,
because that's what it has to be for a driver to trust and use it without
installing anything.

Show a conversation thread with exactly this exchange, in order:

1. Incoming (grey, left): "Marshal: Dock 4 at 14:20 for PR-1041. Reply Y to
   confirm."
2. Outgoing (blue, right): "Y"
3. Incoming (grey, left): "Confirmed. See you at 14:20."
4. [a visible time gap in the thread, e.g. a "2:05 PM" timestamp divider]
5. Incoming (grey, left): "Dock 4 now 14:35 (was 14:20). Reply Y to confirm."
6. Outgoing (blue, right): "Y"
7. Incoming (grey, left): "Confirmed. See you at 14:35."

Every incoming message must stay under roughly 160 characters and always end
with a clear, single-word reply instruction when a reply is expected. Every
driver reply must get an explicit confirmation message back — never leave a
reply unacknowledged in the thread, since a driver who isn't sure their "Y"
registered will just call the number instead, defeating the point of SMS.

Render as a single tall mobile phone screen mockup, portrait, showing the full
conversation thread as described above, in chronological order top to bottom.
```

---

## Notes for whoever adds background material here

- Because this "surface" is really a copy-design exercise, the most valuable thing to add to `background/` isn't images — it's **real driver SMS exchanges from Porterly or any prior project**, if any exist, to check tone and message length against what real carriers actually respond well to.
- D-009's LLM-parsing fallback (free-text replies parsed into structured intent, with a keyword fallback when the model is unreachable) means real driver replies won't always be a clean "Y" — worth mocking a second thread variant showing a messier real reply ("yeah be there in 10") and how the system should respond, since that's the harder and more realistic case.
- If SMS costs or carrier/short-code setup become a real constraint, that changes message frequency (e.g. whether a "now 14:35" reschedule text is sent for every small delay or only past some threshold) — a business decision, not a design one, but it'll change what this thread looks like in practice.

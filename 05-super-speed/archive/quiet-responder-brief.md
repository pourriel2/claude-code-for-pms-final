# Coming back: a way back in for responders who have gone quiet

One-pager · Product, Dispatch · 9 October 2026 · For: Helen Achebe · Draft, not reviewed by engineering

## Problem
Since 4.2, a few available responders have stopped getting callouts, and nothing in the product tells them or their handler why. The Undertow had about 12 pings a week before 12 August, then 11, 4, 1 and 1. His handler Desmond Okafor filed ticket 3096 on 26 August ("He asked me this morning whether his account is still active"), and 3145 on 7 September. Four responders (The Undertow, Farlight, Meteor Mite, Vesper) lost 65 to 74% of their pings, and their missed rate went from 2.4% to 58.9%. The other 12 rose from 2.1% to 13.9%.

Why it sticks: a missed ping costs the same as a turn-down (-0.12) against +0.08 for a yes, and the score never eases back (the 2019 TODO). A responder who is not pinged cannot earn a yes, so they cannot recover. Wen's question about that note was fair, and 4.2 made it expensive.

Kip, who handles Meteor Mite and The Gale, sees it as two cards on one screen telling opposite stories: "I just want it to look less like a coincidence." Nothing on screen explains it. Handlers do not know the ping wait exists (tickets 3047, 3065).

## Who it is for
1. **A quiet responder** (The Undertow is the worked example): available, tags set, in range, and not being offered work.
2. **Their handler** (Desmond Okafor, Kip, Aunt Dot): sees the quiet, cannot tell what it means, and files a ticket or tells the responder to "hang in there".

## What changes for them
- **Responder, on the phone:** a plain status in place of silence. "You're in rotation. No pings for 9 days. Your last 8 offers ran out before you answered, which lowered your place. It eases on its own." Once quiet crosses a set number of days, they get a **first look** at the next callout they are a real fit for (inside the proximity range, capability tags matched). A ping they answer is credited as normal.
- **Handler, in the console:** a "Quiet" badge on the coverage card with pings in the last 7 days and days since the last one, the reason in one line, and a note when it lifts. A handler no longer learns about it from a responder's text at midnight.
- **Under both:** a missed ping costs less than a turn-down, and a score from misses eases back toward neutral over time. A turn-down still sticks until the responder takes work again, which keeps the argument in Wen's 2019 note.

## Success measure (targets are my proposal, to agree with Ravi)
- No available, matched responder goes more than 5 days without a ping.
- The four reach at least 60% of their pre-4.2 weekly pings within three weeks of release.
- New "phone never goes off" tickets: none after release (about 30 filed since 12 August, none closed).
- Guardrails: callouts nobody took stay near 5% (13% for three weeks after 12 August), and pings per callout stay at or below 1.30 (1.23 before 4.2, 1.39 after).
- Time-to-accept cannot be measured today because nothing logs response time. We need that logged first.

## What it deliberately does not do
- It does not change the 4.2 proximity weights or revert the release.
- It does not set the ping wait. Restoring 90 seconds is a separate decision with its own gate on 16 October, and it is the main lever on misses. This brief covers the people the wait already left behind.
- It does not put a non-matching or out-of-range responder first. Capability match and proximity still decide.
- It does not promise any responder a volume of work, or show one responder's score to another.
- No handler-adjustable routing setting. Routing config still ships in the release.
- No legal identity or cover identity mapping of any kind (Security Policy 4.1). No mutual aid (Q4 list).

## Open questions and dependencies
- Wen Li: when does the 60s clock start (send or delivery)? Do scores survive a restart? Are the four scores still at the floor?
- Marcus: can scores be corrected for the four now, and is a first look a one-release change?
- Supply: callout load shifts, and Supply books maintenance into low-load windows from the Responder Availability Record. Tell the Supply PM first.
- Sofia: console badge and phone status design. Prototype alongside: `quiet-responder-prototype.html`.
- Ravi: last August's numbers, and data after 6 September.

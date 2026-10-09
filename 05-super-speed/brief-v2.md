# One-pager: Fixing the quiet-responder problem properly

To: Helen Achebe. Date: 9 Oct 2026. Full detail: `prd-quiet-responder-recovery.md`.

**Owner:** [your name], PM, Rook Dispatch.
**Step owners (proposed):** step 1, Marcus Oyelaran (engineering) with the PM. Step 2, the PM with Marcus, Wen Li (ranking logic) and Sofia Marino (design). Measurement, Ravi Menon. Telling Supply, the PM.

## Scope
- **In:** (1) restore the 90 second wait and reset four rankings, (2) forgiving scoring plus handler and responder views in 4.3, (3) a note to handlers, (4) which Q3 commitment makes room.
- **Out:** mutual aid, a per-handler ping wait, any runtime setting. Routing stays in the release.

## What happened
- 4.2 cut the time to answer a ping from 90 seconds to 60.
- Missed pings went from about 2% to 21.5% (week of 10 Aug). The system counts a miss the same as a turn-down, and only a yes raises a ranking.
- Four responders who were fine before now miss 59% of pings (12 Aug to 6 Sep) and get 65 to 74% fewer. Fewer pings means fewer chances to say yes, so they cannot climb back alone.
- 45 handler tickets about this are still open.

## What we would build, by who feels it

**Kip (handler) will see:**
- A timeline on every callout: "Offered to Meteor Mite, no answer in 90s, offered to The Gale, taken."
- The ping wait shown on the callout, so "it moved on" has an answer.
- An alert when nobody takes a callout, with one click to re-offer. Today it silently returns nothing.

**A responder who has gone quiet will feel:**
- A countdown on the ping, and after a miss, a plain line: "Offered for 90 seconds."
- A route back: after a gap, one ping at fair rank, then scored normally.
- A missed ping that costs less than a turn-down, and rankings that drift back toward neutral.

No scores shown to handlers or responders (counts and plain language instead), no other responders shown to anyone, nothing tied to real identity (Security Policy 4.1).

## Order of work
1. **This release (step 1):**
   - Restore 90 seconds.
   - Reset the four affected rankings, nobody else's.
   - Tell Supply first, because who gets callouts will shift.
   - Watch for two weeks.
2. **4.3 (step 2):** forgiving scoring plus the handler and responder views above. Scope decision by 16 Oct.

A simple test model (invented responders, not real data) suggests 90 seconds alone cuts misses from 19% to 4%. Real results will tell us whether that holds.

## How we will know
Targets are my proposals, not measured. Dates run from the day step 1 ships.

1. **Missed rate, all responders:** from 12.7% (week of 31 Aug) to under 4% within 2 weeks.
2. **Missed rate, the four:** from 58.9% (33 of 56 pings, 12 Aug to 6 Sep) to under 10% within 2 weeks.
3. **Weekly pings, the four:** back within 20% of each one's own average for 29 Jun to 9 Aug, within 4 weeks.
4. **Open callout tickets:** from 45 to 0 within 4 weeks.
5. **Uncovered callouts:** from 5.5% (week of 31 Aug; about 13% for the three weeks after 12 Aug) to about 5% or lower within 2 weeks.

## Measurement plan
1. **What:** the five measures above. Guardrails: turn-downs do not rise, and no area's uncovered rate goes above its pre-4.2 level.
2. **Source:** the pings and callouts data, and support tickets.
3. **Who and when:** Ravi Menon, added to the weekly acceptance-rate report, plus a read at the 2 week mark.
4. **Baseline:** the figures above. Ravi to pull the four responders' pre-4.2 weekly pings.
5. **Decision rule (proposed):** if the four are under 10% missed and back within 20% of old volume, step 2 shrinks to the views and a lighter scoring change. If not, the scoring fix becomes the top 4.3 item.
6. **Cannot measure yet:** time to accept, because response time is not logged.

## Decisions for Helen
1. We should ship step 1 alone, this release. Restore 90 seconds and reset the four rankings, and change nothing else, so we can see what that fix does by itself.
2. We should put the scoring fix in 4.3 scope now and confirm it after the two week read. The wait is only half the problem, because the ranking has no way to forgive a quiet responder. Something has to give to make room, and I suggest we start with Availability Confidence, which was committed for 4.2 and never shipped, and settle which Q3 commitments still stand.
3. We should send the customer note to handlers once step 1 is scheduled. It is drafted and not yet sent.

## Not yet known
- When the 60 second clock starts: send or delivery (Wen Li).
- Whether rankings survive a restart, whether one ranking can be reset, and whether the reward and penalty sizes changed in 4.2 (Marcus).
- Data after 6 Sep and from last August (Ravi).
- Owners above are proposed, not agreed.

## About the test model
- A small script with made-up responders and a simplified ranking, tuned to about 2% misses at 90 seconds and about 19% at 60.
- It shows direction: the wait matters most, and the ranking weights decide who gets starved.
- It cannot say how much a real change will help, which is why we measure.

Click-through of the handler and responder views: `clickthrough-quiet-responder.html`.

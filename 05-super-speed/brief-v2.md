# One-pager: Fixing the quiet-responder problem properly

To: Helen Achebe. Date: 9 Oct 2026. Detail and metrics: `prd-quiet-responder-recovery.md`.

**Owner:** Rebbie Walsh, PM, Rook Dispatch.
**Proposed step owners:** step 1, Marcus Oyelaran with Rebbie. Step 2, Rebbie with Marcus, Wen Li and Sofia Marino. Measurement, Ravi Menon. Not yet agreed.

## What happened
- 4.2 cut the time to answer a ping from 90 seconds to 60.
- Missed pings went from about 2% to 21.5% (week of 10 Aug). A miss counts the same as a turn-down, and only a yes raises a ranking.
- Four responders now miss 59% of pings (12 Aug to 6 Sep) and get 65 to 74% fewer, so they cannot climb back alone.
- 45 handler tickets about this are still open.

## Scope
- **In:** (1) restore 90 seconds and reset four rankings, (2) forgiving scoring plus handler and responder views in 4.3, (3) a note to handlers, (4) which Q3 commitment makes room.
- **Out:** mutual aid, a per-handler ping wait, any runtime setting.

## What we would build, by who feels it
**Kip (handler) will see:**
- A timeline on every callout: "Offered to Meteor Mite, no answer in 90s, offered to The Gale, taken."
- The ping wait shown on the callout.
- An alert when nobody takes a callout, with one click to re-offer.

**A responder who has gone quiet will feel:**
- A countdown on the ping, and after a miss: "Offered for 90 seconds."
- A route back: after a gap, one ping at fair rank, then scored normally.
- A missed ping that costs less than a turn-down, and rankings that drift back toward neutral.

No scores shown to anyone, only counts. Nothing tied to real identity (Security Policy 4.1).

## Order of work
1. **This release:** restore 90 seconds, reset the four affected rankings only, tell Supply first, watch for two weeks.
2. **4.3:** forgiving scoring plus the views above. Scope decision by 16 Oct.

A test model with invented responders suggests 90 seconds alone cuts misses from 19% to 4% (`00-rook/analysis/ping-sim.py`). Real results have to confirm it.

## How we will know
Targets are my proposals, not measured. Dates run from the day step 1 ships.
1. Missed rate, all responders: 12.7% (week of 31 Aug) to under 4% in 2 weeks.
2. Missed rate, the four: 58.9% (12 Aug to 6 Sep) to under 10% in 2 weeks.
3. Weekly pings, the four: back within 20% of their own 29 Jun to 9 Aug average in 4 weeks.
4. Open callout tickets: 45 to 0 in 4 weeks.
5. Uncovered callouts: 5.5% (week of 31 Aug) to about 5% or lower in 2 weeks.

Ravi reports weekly, with a read at two weeks. If the four are under 10% missed, step 2 shrinks to the views and a lighter scoring change. If not, the scoring fix becomes the top 4.3 item. Sources, guardrails and the full plan: PRD section 6.

## Decisions for Helen
1. We should ship step 1 alone, this release, so we can see what that fix does by itself.
2. We should put the scoring fix in 4.3 scope by 16 Oct. Something has to give, and I suggest we start with Availability Confidence, committed for 4.2 and never shipped.
3. We should send the customer note to handlers once step 1 is scheduled. It is drafted, not sent.

## Not yet known
- When the 60 second clock starts, at send or at delivery (Wen Li).
- Whether one ranking can be reset, whether rankings survive a restart, and whether the reward and penalty sizes changed in 4.2 (Marcus).
- Data after 6 Sep and from last August (Ravi).

Click-through of the handler and responder views: `prototype.html`.

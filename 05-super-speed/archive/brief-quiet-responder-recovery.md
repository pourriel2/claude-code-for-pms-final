# One-pager: Fixing the quiet-responder problem properly

To: Helen Achebe. From: PM, Rook Dispatch. 9 Oct 2026. Full detail: `prd-quiet-responder-recovery.md`.

## What happened
4.2 cut the time a responder has to answer a ping from 90 seconds to 60. Missed pings jumped from about 2% to 21.5%. The system treats a missed ping the same as a turn-down, and the only thing that raises a responder's ranking is saying yes. So four responders who were fine before 4.2 now miss 59% of pings and get 65 to 74% fewer pings. Fewer pings means fewer chances to say yes, so they cannot climb back on their own. 45 handler tickets about this are still open.

## What we would build, by who feels it

**Kip (handler) will see:**
- A timeline on every callout: "Offered to Meteor Mite, no answer in 90s, offered to The Gale, taken."
- The ping wait shown on the callout, so "it moved on" has an answer.
- An alert when nobody takes a callout, with one click to re-offer. Today it silently returns nothing.

**A responder who has gone quiet will feel:**
- A countdown on the ping, and after a miss, a plain line: "Offered for 90 seconds."
- A route back: after a gap, they get one ping at fair rank, then are scored normally.
- A missed ping that costs less than a turn-down, and scores that drift back toward neutral instead of staying low forever.

No scores shown to handlers, no other responders shown to anyone, and nothing tied to real identity (Security Policy 4.1).

## Order of work
1. **This release:** give responders their 90 seconds back and reset the four affected responders' rankings, nobody else's. Tell Supply first, because who gets callouts will shift. Then watch for two weeks. In a simple test model I built (invented responders, not real data), 90 seconds alone cut missed pings from 19% to 4%. Real results will tell us whether that holds.
2. **4.3:** forgiving scoring plus the handler and responder views above. Decision on this by 16 Oct.

## How we will know
Missed rate under 4% (now 12.7%). Four affected responders under 10% missed and back within 20% of old ping volume. 45 open tickets to zero. Uncovered callouts back to about 5%.

## Decisions for Helen
1. We should ship step 1 alone, this release. Restore 90 seconds and reset the four rankings, and change nothing else, so we can see what that fix does by itself.
2. We should put the scoring fix in 4.3. The wait is only half the problem, because the ranking has no way to forgive a quiet responder. Something has to give to make room, and I suggest we start with Availability Confidence, which was committed for 4.2 and never shipped, and settle which Q3 commitments still stand.
3. We should send the customer note to handlers once step 1 is scheduled. It is drafted and not yet sent.

## Not yet known
- When the 60 second clock starts: when we send the ping, or when it reaches the phone (Wen Li).
- Whether rankings survive a restart, and whether the reward and penalty sizes changed in 4.2 (Marcus).
- Data after 6 Sep and from last August (Ravi).
- The targets above are my proposals, not measured.

## About the "test model"
I built a small simulation in a script: made-up responders, simplified ranking, tuned until it gave about 2% misses at 90 seconds and about 19% at 60, which matches what we saw. Then I changed one thing at a time. It shows the direction (the wait matters most, the ranking weights decide who gets starved). It is not real data and it cannot say how much a real change will help, which is why we measure for two weeks.

**Next:** click-through of the handler timeline and responder phone view.

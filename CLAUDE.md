# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I am the new PM for Rook Dispatch, taking over from Priya Raghunathan (left 21 Aug 2026, no overlap). Sources: Priya's handoff doc (`00-rook/company/notes/handoff-from-priya.docx`) and the Rook wiki (read via the rook-wiki connector). Today is early Oct 2026.

### Company and products
- Rook Industries, founded 2014, 241 staff, HQ at Site Aleph (ice shelf, twice-weekly transport, mostly remote). Offices in Berlin and Singapore (plus a lighthouse in Cornwall).
- Customers are independent masked responders and their handlers and quartermasters. Rook employs no responders. Revenue is subscription, per active responder.
- Monthly release train, 4.x numbering. Support has three tiers; tickets filed mid-callout skip the queue.
- **Rook Dispatch (mine, release 4.2):** ranks available responders for an incident, pings the top one's phone, they take it or not, else it moves down the list. Handlers use the web console; responders use the phone app. Routing config ships in the release, not as a runtime setting.
- **Rook Supply (4.2):** gear requisitions, quartermaster approval, maintenance schedules, field failure reports.
- **Dispatch to Supply dependency:** Supply reads the Responder Availability Record, which Dispatch writes, and books maintenance into low callout-load windows. Any change to how Dispatch calculates availability or callout load changes Supply's scheduling with no Supply-side change.

### Hard rules from the wiki
- Never store or infer responder legal identity. Cover identities are never mapped in production (Security Policy 4.1). Do not design features that assume a mapping, and do not try to work out who anyone is.

### People (Dispatch)
| Name | Role | Notes |
| --- | --- | --- |
| Helen Achebe | Director of Product (my boss) | Owns roadmap and commitments. Gives room. |
| Marcus Oyelaran | Eng Manager, Dispatch | Site Aleph. Priya's first call for anything uncertain. |
| Wen Li | Staff Engineer | Berlin. Built the ping-ranking logic. No doc exists, so ask her. Was away 14-24 Aug, i.e. right after 4.2 shipped. |
| Nadia Hoffmann | Support Lead | Berlin. Hears handler complaints first. Worth a standing 15 minutes. |
| Ravi Menon | Data Analyst | Singapore. Owns the weekly acceptance-rate report. |
| Sofia Marino | Product Designer | Console and phone app. Ran the September interviews (not yet read). |

Priya's doc says Marcus pulls numbers; the directory says Ravi owns them. Try Ravi first for metrics.

### Vocabulary
- **Callout:** request for a responder to attend an incident. **Ping:** a callout offered to one responder. **Taken / turned down / missed:** the three outcomes. Turned down and missed both pass it on but are recorded separately.
- **Ping wait:** seconds before an unanswered ping counts as missed. Same for everyone, set in the release.
- **Routing priority:** score ranking responders. Inputs: proximity (travel-time estimate), availability, capability match, recent acceptance history. Turning down or missing a ping lowers recent acceptance, which lowers later rank.
- **Acceptance rate:** pings taken / pings sent. Headline metric, reported weekly in aggregate. **Time-to-accept:** median seconds from ping to taken.
- **Coverage gap:** no available responder had the required capability tags. Not the same as low acceptance (nobody could go vs nobody would).
- **Capability tags:** flight, structural-entry, hazmat-tolerant, cold-weather, aquatic, crowd-management, de-escalation.
- **Mutual aid:** cross-area cover between responders. Not supported, on the Q4 list.

### Release history (Dispatch)
- 4.0 (7 Apr): new console nav, responder profile redesign, routing-override audit log.
- 4.1 (16 Jun): travel-time proximity, bulk callout, push delivery reliability.
- 4.2 (12 Aug): proximity weighted up vs recent acceptance, ping wait cut 90s to 60s, console filters persist, three fixes.

### Where things stand
1. **Acceptance has dropped since 4.2 and handler complaints are up.** Two changes shipped together (ranking and ping wait cut), on top of a seasonal August dip. Priya's view is mostly seasonal, back in September, and she urged against reverting 4.2 (proximity was a three-quarter-old responder ask). That is her read, not a measured result. Nothing in these sources shows September numbers, so check with Ravi before accepting or rejecting it.
2. **Possible compounding effect (my inference, untested):** a shorter ping wait should raise "missed" counts, and misses lower recent-acceptance scores, which lowers rank. Worth checking whether the drop is partly self-reinforcing.
3. **Roadmap is stale.** Q3 roadmap was last reviewed 30 Jun. It lists *Availability Confidence* as committed for 4.2, but it is absent from the 4.2 release notes. Priya said a couple of items were squeezed out and the conversation with Helen about which are still Q3 commitments has not happened. Needs to happen soon.
4. **Other roadmap items:** Requisition approval chains (Supply, committed for 4.3); Handler phone app and Shared cover between responders (both Q4, exploring). Committed items go through Product to change, not directly.
5. **Known noise:** console filter persistence will generate cosmetic tickets. Do not let it eat the first month.
6. **Debt:** no written description of how ping ranking works. Priya asked me to write it, with Wen Li.

### Where to look
- Wiki: Company page (About Rook, Rook Dispatch, Rook Supply, Glossary, Team directory, Releases, Q3 roadmap).
- A rook-database connector is also available (not yet explored; likely the source for acceptance data).
- Priya's last line of advice: I arrive with no attachment to past decisions, and that advantage fades, so use it in month one.

- Session 1 (6 Oct 2026) findings. Database (29 Jun to 6 Sep): missed pings went from about 2% to 21.5% in the week of 12 Aug, turn-downs did not rise, and misses are concentrated in a few responders (The Undertow, Farlight, Meteor Mite, Vesper) who now get far fewer pings. Pings per callout: 1.23 before 4.2, 1.39 after.
- Code (`00-rook/code/dispatch-routing/`, stubs only): a miss costs the same as a turn-down (-0.12) against +0.08 for a yes, with no decay (2019 TODO). This supports the feedback loop with the 60s wait. Ranking weights moved 0.45/0.40 to 0.60/0.25 in 4.2.
- Wiki and handoff have nothing on competitors or churn. The wiki says "monthly" releases but 4.0 to 4.2 took 8 to 10 weeks, and no 4.3 is listed.
- Plan is in `00-rook/project-plan.md`. Proposed default: restore ping wait to 90s alone, measure two weeks, decision by 16 Oct. Draft message to Marcus on this was written, not sent.
- Still open: data after 6 Sep (ask Ravi), Sofia's September interview notes, why 60s was chosen, what Availability Confidence was, and the definition of an active responder.
- Session 2 (6 Oct 2026) findings. Four September interviews (wiki, 2 to 5 Sep) and 147 support tickets (database, 29 Jun to 7 Sep) agree on the headline. Tickets went from about 6 a week (40, all closed) to about 28 a week (107, 83 open). Two new themes start on 12 Aug and none of their 45 tickets is closed: callout moved on before the responder could answer (15, 11 of 12 handlers) and responder gone quiet (30, four handlers).
- Pings per responder per week, before vs after 12 Aug: Farlight, The Undertow, Meteor Mite, Vesper down 65 to 74%; Halfmoon and Corporal Ashgrove down about 16 to 19%; The Gale up 48% and Sgt. Falkirk up 44%. Total pings stay flat (about 170 a week). Missed rate 21.5% (week of 10 Aug) eased to 12.7% (week of 31 Aug), still about 6x baseline. The easing may partly be the starved responders being pinged less (my inference).
- Ticket volume does not track harm. Aunt Dot (Vesper) and Kip (Meteor Mite, The Gale) filed zero tickets; three of the four interviewees are non-filers, so interviews and tickets heard from mostly different people. Interviews gave the mechanism, tickets the scale. Handlers do not know the ping wait exists (tickets 3047, 3065), and tickets say "thumb on the screen" (3041, 3055, 3056).
- Support has closed none of the 45 callout tickets, and nothing filed after 27 Aug is closed; the table has no reply column. Ask Nadia. Many open tickets repeat one closed earlier (27 of 45 non-callout issues after 12 Aug were already reported before). Other tickets worth routing: Supply safety items (vest plate 3074, grapple line 3092, requisition 3128), duplicate responder on invoices (3023, 3075), screen reader gap (3039, 3137), silent filter reset and 20-minute sign-out (3044, 3072, 3134, 3107), phone number rejected and availability time zone (3132, 3116).
- Working hypothesis, untested: the 60s wait plus the equal miss penalty with no decay starved four responders, so restoring 90s alone may not recover them. Ask Wen Li when the 60s timer starts (send or delivery). Ask Marcus whether a score correction is possible.
- No `dispatch-priorities.md` exists in this folder; the task list is `00-rook/project-plan.md`. A proposed re-ordering with 7 new tasks was given in chat only and is not saved.
- Session 3 (7 Oct 2026) findings. Saved to this folder: `00-rook/data/callout-history.csv` (weekly pings sent and taken per responder, 29 Jun to 31 Aug), the company wiki pages and 4.2 comments in `00-rook/company/`, four interviews, 147 tickets as `00-rook/feedback/tickets/t-<number>.txt`, and four product briefs in `06-sidekicks/briefs/`. Time-to-accept cannot be calculated: the database has no response time.
- Missed rate, split at 12 Aug: the four starved responders went from 2.4% to 58.9% (33 of 56 pings), the other 12 from 2.1% to 13.9% (11.1% in the week of 31 Aug). Every one of the 16 rose and none is below 10%. Acceptance was 76.8% before, 54.2% in the 4.2 week, 68.5% for 17 to 31 Aug. Misses jump on 12 Aug itself (7 that day, 12 on the 13th); the first callout ticket (3041) came 12 Aug at 15:41, "gone quiet" tickets from 17 Aug.
- Seasonal story (Priya): callouts were about 11% lower in August (19.7 to 17.5 a day) but pings stayed flat, and a step on release day plus four responders losing 80% of pings is not seasonal. No prior-year data exists to test "August is always soft", so ask Ravi for last August.
- The Undertow is the worked example: normal pings 12 to 16 Aug but 5 of his first 8 missed, then pings fell 11, 4, 1, 1 a week, with no ping for 9 days (27 Aug to 5 Sep). In the code stub a yes is +0.08 and a miss -0.12, so a score only rises above 60% acceptance, and with no decay a quiet responder cannot recover on their own.
- Uncovered callouts (no ping taken) were about 5% before, about 13% for three weeks after 12 Aug and 5.5% in the week of 31 Aug; the rise is in Southport, Riverside and Kingsbridge, not the starved responders' areas (small counts, 6 to 9 each). Plan: lead with unanswered callouts for leadership and keep the missed rate as the cause.
- Four handlers filed 0 or 1 tickets (Aunt Dot, Kip, Halloran, Ambrose), the same four as the interviews, and Vesper and Meteor Mite are among the worst hit. Nadia's 26 Aug note says a handler emailed her directly, so ask who. Still open: when the 60s timer starts (Wen Li), last year's August (Ravi), data after 6 Sep, and why uncovered rose in three areas.
- Session 4 (7 Oct 2026) findings. Code read in full (stubs): the only thing that raises a score is a yes (+0.08), called from one place in `offer.py`. No decay, no reset, no new-versus-existing split. Missed and turned down both go through `record_declined` (-0.12, floor 0). Scores sit in a memory dictionary, so a restart may reset everyone (unverified). Nothing logs response time, and when the list runs out `dispatch` returns nothing with no retry or alert.
- Only the weights and the wait have a "was" note or changelog entry; ask Marcus whether +0.08 and -0.12 moved. Nearness is 0.60 of the ranking, so a score of 0 vs 0.5 costs about 9 minutes of travel: a clearly nearest quiet responder can still rank first. The four hardest hit had ordinary acceptance before 4.2 (68.7 to 81.9%), so the change did not target people already turning jobs down. That answers Marcus's 14 Aug question (reply drafted, not sent).
- Simulation in `00-rook/analysis/ping-sim.py` (toy model, invented responders, tuned to about 2% and 19% misses): the wait is the main lever on misses (restoring 90s alone takes 19% to 4%); the weights decide who is starved. The miss penalty barely mattered alone, but the model has no sticky slow responders, so do not lean on that. Options short of a reset: score floor, ease toward neutral, quiet-responder rule, split missed from turned down. Suggested test: restore 90s and reset only the four scores; tell Supply first (callout load shifts).
- Drafted, not sent: a customer note (needs Helen's OK) and a Marcus message. Still open: current scores for the four, when the 60s clock starts, whether scores survive a restart, whether anything outside this folder changes scores, how location is set, what happens when the list runs out.
- Session 5 (9 Oct 2026) findings. Helen's memo (`05-super-speed/director-request.txt`) asks for a one-pager and something clickable on what we would build instead of quietly changing a number, seen from the person it happens to (Kip the handler, a responder who has gone quiet). Saved in `05-super-speed/`: `prd-quiet-responder-recovery.md`, `brief.md` (same as `brief-quiet-responder-recovery.md`) and `clickthrough-quiet-responder.html` (comic-book responder phone app, plain handler console, Today vs Proposed switch). The wrap-up check looks for `prototype.html`, which does not exist; the click-through has the longer name. Two other files, `quiet-responder-brief.md` and `quiet-responder-prototype.html`, appeared in that folder and I did not write them.
- The plan in the brief: step 1 this release is restore 90s and reset only the four affected scores, tell Supply first, measure two weeks. Step 2 in 4.3 is forgiving scoring (split missed from turned down, ease toward neutral, quiet-responder rule) plus a handler callout timeline and re-offer, and a responder countdown and miss message. Decisions for Helen: ship step 1 alone, put the scoring fix in 4.3 (make room by looking at Availability Confidence), send the customer note once step 1 is scheduled. Nothing has been sent. Position taken: no scores shown to handlers or responders, only counts and plain language.
- Gaps before anything can be built: whether per-ping events exist to power the timeline, what counts as quiet and who sees it, what re-offer means (retry logic is new, and should log to the 4.0 routing-override audit log), whether a quiet rule can override nearness at 0.60 so the promise 'you will be considered for your next callout' holds, when the 60s clock starts, whether one score can be reset, and no engineering estimate beyond the one-number change. The prototype fixes nothing by itself; restoring 90s and the scoring change are the fix. Next-steps cards, turn-down reason chips and the 'My last month' chart are new ideas not yet in the PRD or brief.
- Meteor Mite (Kip's responder) in the database: 44 pings 13 Jul to 9 Aug (30 taken, 12 turned down, 2 missed) against 17 pings 10 Aug to 6 Sep (5 taken, 4 turned down, 8 missed). Last ping 5 Sep. Weekly pings from 10 Aug: 10, 4, 2, 1. The Undertow's 9 days with no ping is his, not Meteor Mite's.

# PRD: Quiet Responder Recovery (Rook Dispatch, target 4.3)

Author: PM, Rook Dispatch. Status: Draft for Helen Achebe. Date: 9 Oct 2026.
Responds to: `05-super-speed/director-request.txt` (Helen, "what would we actually build, from the point of view of the person it happens to").

## 1. Summary

Release 4.2 (12 Aug) cut the ping wait from 90s to 60s and shifted ranking toward proximity. Misses rose from about 2% to 21.5% overnight. Because a missed ping costs a responder the same as a turn-down (-0.12) and nothing ever raises a score except a yes (+0.08), four responders were starved of pings and cannot recover on their own. Handlers see callouts moving on before a responder could answer, and neither side can see why.

The quick fix is one number (90s). This PRD covers what to build instead: a restore of the wait plus a ranking that can forgive, and visible feedback for the handler and the responder, so the system stops silently punishing people for slowness it caused.

## 2. Problem

### Who it happens to

**Handler (example: Kip).** A callout "moves on" before the responder they expected had a chance to answer. They do not know a ping wait exists (tickets 3047, 3065), cannot see who was pinged or why it moved, and cannot tell a coverage problem from a responder who is simply quiet. 15 tickets on "callout moved on" (11 of 12 handlers) and 30 on "responder gone quiet" (4 handlers). None of those 45 is closed. Some handlers filed nothing at all but are among the most affected.

**Responder who has gone quiet (example: The Undertow).** Normal pings 12 to 16 Aug, 5 of the first 8 missed, then pings fell 11, 4, 1, 1 a week, with no ping for 9 days. Nothing in the phone app says their rank dropped, why, or what would bring it back. Several interviewees and tickets describe a "thumb on the screen" problem: they are ready but the ping lapses first.

### Evidence

| Signal | Before 12 Aug | After |
| --- | --- | --- |
| Missed pings | about 2% | 21.5% (week of 10 Aug), 12.7% (week of 31 Aug) |
| Four starved responders, missed rate | 2.4% | 58.9% (33 of 56) |
| Other 12 responders, missed rate | 2.1% | 13.9% (11.1% week of 31 Aug) |
| Pings per callout | 1.23 | 1.39 |
| Uncovered callouts (no ping taken) | about 5% | about 13% for 3 weeks, 5.5% week of 31 Aug |
| Support tickets per week | about 6 | about 28 |
| Acceptance rate | 76.8% | 54.2% (4.2 week), 68.5% (17 to 31 Aug) |

Those four had ordinary acceptance before 4.2 (68.7 to 81.9%), so this did not target people who were already turning jobs down. Callouts were about 11% lower in August but pings stayed flat, so seasonality does not explain a step on release day.

### Root causes (from code review, stubs only)

1. Ping wait 60s for everyone, set in the release.
2. A miss and a turn-down are the same event to the score (`record_declined`, -0.12, floor 0). A yes is +0.08, so a score only rises above 60% acceptance.
3. No decay, no reset, no new-versus-existing split (2019 TODO from Wen Li). A quiet responder is pinged less, so gets fewer chances to earn a yes. The loop does not end by itself.
4. Nearness is 0.60 of the ranking after 4.2 (was 0.45), so low-acceptance responders sink faster.
5. When the ranked list runs out, `dispatch` returns nothing: no retry, no alert.

## 3. Goals and non-goals

### Goals
- A quiet responder who is ready and willing gets pinged again without needing a manual fix.
- A handler can see what happened to a callout and why it moved on.
- Misses caused by too short a window stop counting as refusals.
- Total uncovered callouts return to the pre-4.2 level (about 5%).

### Non-goals
- No change to how capability tags or proximity work.
- No mutual aid (Q4 list).
- No per-handler ping wait, no runtime setting. Routing config stays in the release.
- Nothing that stores, infers or maps a responder's legal identity (Security Policy 4.1). All designs below use cover identities only.

## 4. Proposed solution

### Stage 0: restore the ping wait to 90s (this week, alone)
Smallest change that attacks the cause with most effect. In the toy simulation, restoring 90s alone takes misses from 19% to 4%. Measure for two weeks. Tell Supply first, because callout load shifts and Supply books maintenance into low-load windows.

### Stage 1: scoring that can forgive (4.3)
Pick one from this list, then confirm with Wen Li and Marcus:
- **Split missed from turned down.** A miss costs less than a turn-down, or nothing while the wait is under a floor.
- **Ease toward neutral.** A score drifts back toward the midpoint over time with no new events.
- **Quiet-responder rule.** A responder with no ping in N days is offered one ping at a fair rank, then scored normally.
- **Score floor.** Keep nearest-responder advantage from being erased by a bad two weeks.

One-time correction: reset only the scores of the four affected responders to neutral, on the same day as the 90s restore. Do not reset everyone.

### Stage 2: what each person sees
**Handler console.** A callout timeline: "Offered to Meteor Mite, no answer in 90s, offered to The Gale, taken." The ping wait shown on the callout view. An alert when the list runs out with nobody taking it, with a one-click re-offer to the next tier. Handlers do not need to see scores.

**Responder phone app.** A visible countdown on the ping. After a missed ping: "You missed a callout. It was offered for 90 seconds." A plain-language line on what affects how often they are pinged, and a quiet "you will be offered the next callout in your area" when they return after a gap. Nothing that reveals other responders.

### Click-through
A prototype of the two views (handler timeline and re-offer, responder missed ping and return) is Stage 2's design input. Sofia Marino to build with me.

## 5. Users and use cases

| User | Need | Success looks like |
| --- | --- | --- |
| Handler | Know what is happening to a callout mid-incident | Can answer "who was asked and why did it move" without filing a ticket |
| Responder (active) | Not be penalised for the timer | Misses fall to near baseline |
| Responder (quiet) | A route back to being pinged | Pinged again within a set window, no support ticket |
| Quartermaster, Supply | Stable callout-load picture | Told before availability or load calculations change |

## 6. Success metrics

Report weekly, in aggregate, by Ravi Menon. Definitions use pings taken / pings sent for acceptance.

| Metric | Baseline | Target |
| --- | --- | --- |
| Missed rate, all responders | 12.7% (wk of 31 Aug), 2% pre-4.2 | under 4% within 2 weeks of Stage 0 |
| Missed rate, the four affected | 58.9% | under 10% |
| Pings per week, the four affected | down 65 to 74% | back within 20% of pre-4.2 |
| Uncovered callouts | 5.5% | about 5% or lower |
| Open "moved on" and "gone quiet" tickets | 45 open | 0 open, new ones under 5 a week |
| Pings per callout | 1.39 | 1.25 or lower |

Guardrails: no rise in turn-downs, no fall in time-to-accept once measurable, no rise in uncovered callouts in any single area.

Measurement plan:
1. **Sources:** the pings, callouts and support_tickets tables in the Rook database.
2. **Owner and cadence:** Ravi Menon, added to the weekly acceptance-rate report, plus a read at two weeks after Stage 0 ships.
3. **Baselines:** the table above. Ravi to pull each of the four responders' own average weekly pings for 29 Jun to 9 Aug.
4. **Decision rule (proposed):** if the four are under 10% missed and back within 20% of their own volume, Stage 1 shrinks to the views and a lighter scoring change. If not, the scoring fix becomes the top 4.3 item.
5. **Cannot measure yet:** time-to-accept, because response time is not logged.
6. **Targets and owners are proposals, not agreed.**

## 7. Dependencies and risks

- **Supply.** Supply reads the Responder Availability Record and books maintenance into low-load windows. Any change to availability or callout load shifts Supply's scheduling with no Supply-side change. Notify before Stage 0.
- **Restoring 90s alone may not recover the four.** Their scores are low and there is no decay. Hence Stage 1.
- **Longer wait slows handoff to the next responder** in a real emergency. Needs Marcus and Helen to agree the trade (about 30s per ping that goes unanswered).
- **Scores may live in memory** (unverified). A restart could reset everyone, which would hide the problem and confuse the measurement.
- **Roadmap.** Availability Confidence was committed for 4.2 and missing from release notes. Needs the conversation with Helen about what is still a Q3 commitment. 4.3 scope is not yet settled.

## 8. Open questions (owner)

1. Does the 60s clock start at send or delivery? (Wen Li)
2. Did +0.08 and -0.12 move in 4.2? Can scores be corrected? Do they survive a restart? (Marcus)
3. Why was 60s chosen? (Marcus, Wen Li)
4. Data after 6 Sep, and last August for the seasonal test. (Ravi)
5. Why did uncovered callouts rise in Southport, Riverside and Kingsbridge? (Ravi)
6. Who is a responder "active" for billing? Affects the quiet-responder rule. (Helen, Marcus)
7. Why are 45 callout tickets all open, and which handler emailed Nadia directly on 26 Aug? (Nadia)
8. Is the miss penalty a real issue or only matters with the 60s wait? The toy model says the penalty barely mattered alone but has no sticky slow responders, so this needs real data.

## 9. Rollout

1. Notify Supply, Support (Nadia) and handlers. Customer note needs Helen's OK (drafted).
2. Stage 0 on the next release: 90s plus a reset of the four scores.
3. Two-week measure. Decision on Stage 1 by 16 Oct.
4. Stage 1 and Stage 2 in 4.3, with Sofia's click-through reviewed by two handlers before build.

## 10. Decisions needed from Helen

- Agree Stage 0 ships first, alone, with the four-score reset.
- Agree the problem is the scoring loop, not just a number, so Stage 1 enters 4.3 scope.
- Agree what drops from 4.3 or Q4 to make room.

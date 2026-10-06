# Rook Dispatch: first-month plan (6 Oct to 6 Nov 2026)

## Goals
1. Stop the missed-ping problem from 4.2 and confirm its cause.
2. Reset the Q3 roadmap with Helen so every commitment has a real owner and date.
3. Write down how ping ranking works (Priya's open ask).
4. Set up weekly signals so the next problem shows up in days, not weeks.

## What I know and don't (as of 6 Oct)
- Known: missed pings went from about 2% to 21.5% in the week of 12 Aug, then eased to 12.7% by the week of 31 Aug. Misses are concentrated in a few responders. Ticket volume roughly quadrupled.
- Known from code: a miss costs the same as a turn-down (-0.12) and a yes earns +0.08, with no decay.
- Unknown: anything after 6 Sep, prior-year seasonality, whether ping wait or ranking change is the main cause, why 60s was chosen, what Availability Confidence was, any competitor or churn data.

## Phase 1: Triage (6 to 9 Oct)
| Task | With | Done when |
| --- | --- | --- |
| Ask if ping wait can ship alone as a point release, and how fast | Marcus | Written answer with a date |
| Get weekly outcomes after 6 Sep | Ravi | Data through last week |
| Per-responder miss and ping-count breakdown | Me (rook-database) | One table, before vs after 12 Aug |
| Book standing 15 min | Nadia | On calendar |
| Book ranking walkthrough | Wen Li | On calendar |
| Book commitments review | Helen | On calendar |

## Phase 2: Diagnose and decide (12 to 16 Oct)
- Ranking walkthrough with Wen Li. Ask: what she expected 60s to do, how misses flow into rank, what Availability Confidence was.
- Read Sofia's September interview notes. Request them if not shared.
- Talk to 3 handlers with the most tickets (Desmond Okafor, Linda Pruitt, Simone Fischer) and, through them, 2 to 4 high-miss responders.
- **Decision gate, 16 Oct:** one-page recommendation to Helen and Marcus.
  - Default proposal: restore ping wait to 90s alone, because it is one config value and easy to reverse. Leave the ranking change in place. Measure for two weeks.
  - This is my inference, not proven. The two changes shipped together, so the data cannot fully separate them.
  - Only change this if Ravi's newer data shows misses back near baseline.

## Phase 3: Fix and reset (19 to 23 Oct)
- Ship or schedule the decided change. Note 4.3 has no date, so agree a ship date with Marcus.
- Roadmap review with Helen:
  - Which 4.2 deferrals (Availability Confidence and others) are still Q3 commitments, and which are dropped.
  - New owner and date for every item. All are currently owned by Priya.
  - Where 4.3 and Requisition approval chains stand, with the Supply PM.
- Sync with the Supply PM: how maintenance windows are chosen, and the marathon-day booking ticket.

## Phase 4: Foundations (26 Oct to 6 Nov)
- Write the ranking spec with Wen Li: inputs, weights, penalty and credit, no decay, how a miss differs from a turn-down. Decide whether the 2019 decay TODO is worth doing.
- Define the weekly dashboard with Ravi (signals below).
- Ask Helen who owns competitor and churn analysis. If nobody, scope a small one.
- Read the first two weeks of post-fix data and write the result up for Helen.

## Weekly signals
1. Missed rate, separate from acceptance rate.
2. Pings per callout (1.23 before 4.2, 1.39 after).
3. Share of misses from the top 5 responders, and their ping counts.
4. Tickets per week, tagged "moved on too fast" vs filter noise.
5. Coverage gaps and time-to-accept.

## Risks
| Risk | Mitigation |
| --- | --- |
| Data ends 6 Sep, so conclusions may be stale | Get Ravi's latest first |
| Fix proves it was the ranking change, not ping wait | Phase 3 measurement; ranking weights are the next lever |
| Changing availability logic breaks Supply scheduling | Sync with Supply PM before any change |
| Wen Li is a single point of knowledge | Do the spec in Phase 4 |
| Helen's commitments conflict with the plan | Hold roadmap review before shipping |
| Responder identity | Never infer or store legal identity (Security Policy 4.1) |

## Open questions to close
- Why was 60s chosen, and who approved it?
- What does "active responder" mean for billing?
- Is there any competitor or churn data?

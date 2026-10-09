---
name: review-checklist
description: Reviews a product brief against the PM's six standing checks (owner, success measure, scope match, problem before fix, succinct format, measurement strategy). Use when the PM says "review this brief", "run the review checklist", "check this brief", or points at a brief file or pasted brief before it goes any further.
---

# Review checklist

Run the same six checks on any brief, every time. The PM should never have to explain the checks again.

## Input

- A file path to a brief (markdown, text, or docx), or brief text pasted into the chat.
- If neither is given, ask once: "Which brief should I review?"
- Read the whole brief before judging it.

## The six checks

1. **Owner.** The brief names who owns it, as a named person, not just a team or "PM". Also look for owners on the decisions and open questions.
2. **Success measure.** It says how we will know it worked: a metric or observable outcome, with a baseline, a target and a time frame.
3. **Scope match.** The scope at the end matches the scope at the start. Compare what the opening says is covered with what the ending asks for, delivers or schedules. List anything that appears at only one end.
4. **Problem before fix.** The problem is explained, with evidence, before any solution is proposed. Flag any fix that appears first, or a problem section that is only a restatement of the fix.
5. **Succinct format.** Short, with bullets for sets and numbered lists for sequences and decisions. Flag long paragraphs and walls of text. A brief should stay brief:
   - Roughly one page. Flag a brief that runs well past that.
   - Flag any section that is long, more than about 6 lines or 4 bullets, and say whether to summarize it or move the detail to a larger document and link to it.
   - Prefer a one or two line summary plus a link (for example to a PRD or analysis) over pasting detail into the brief.
   - Flag anything that explains the same point twice, or that is background rather than something the reader must decide or know.
6. **Measurement strategy.** It lays out how the product will be measured: what is measured, data source, who reports it, how often, baseline, guardrail metrics and what result triggers what decision. This is separate from check 2: check 2 is the goal, check 6 is the plan to measure it.

## How to judge

- Mark each check **Pass**, **Partial** or **Fail**.
- Base every mark on what the brief actually says. Quote or point to the section. Never assume something is covered because it would normally be.
- Do not invent owners, numbers or metrics to make a check pass.
- If a check does not apply, say so and why. Do not skip it silently.

## Output

Keep it short and scannable. Use this layout:

```
Brief: <title or file name>
Verdict: <Ready to go on / Fix first> (<n> of 6 pass)

1. Owner: <Pass/Partial/Fail>
   - Evidence: <quote or section>
   - Fix: <one line, only if not Pass>
2. Success measure: ...
3. Scope match: ...
4. Problem before fix: ...
5. Succinct format: ...
6. Measurement strategy: ...

Top 3 fixes, in order:
1. ...
2. ...
3. ...
```

- Verdict is "Ready to go on" only if all six pass. Anything else is "Fix first".
- List the top fixes in order of impact, at most 3. If everything passes, say so and stop.
- End with one concrete next action the PM can do in under 2 minutes.

## Keep fixes brief too

- A fix must not make the brief longer than it needs to be. When a missing item needs more than a few lines (for example a full measurement plan), recommend a short summary in the brief plus a link to where the detail lives.
- When a brief is too long, name the 2 or 3 sections to cut or summarize first and what the short version should say.
- If the brief already links to a larger document, point to that link as the place for detail instead of asking for it in the brief.

## Do not

- Do not rewrite or edit the brief unless the PM asks. Review only.
- Do not add checks of your own. If something else looks wrong, add one line after the fixes under "Also noticed", at most 2 items.
- Do not review the quality of the idea itself, only these six checks.

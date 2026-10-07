"""What-if simulation of Dispatch ping routing.

A toy model, not Rook's real system. It copies the rules in
code/dispatch-routing (score = weighted proximity + recent acceptance +
capability, ask down the list, wait N seconds, miss costs points) and
adds invented responders and invented response times.

Calibrated to two facts from the database:
  - at 90s about 2% of pings are missed, at 60s about 19-21%
  - about 77% of pings are taken before 4.2
Everything else (positions, response speeds, turn-down habits) is made up,
so read the RESULTS AS DIRECTION, not as forecasts.
"""

import math
import random
import statistics as st

N_RESP = 16
CALLOUTS_PER_WEEK = 122
WARM_WEEKS = 4      # everyone runs on the old settings first
TEST_WEEKS = 8      # then the scenario takes over
P_AVAILABLE = 0.35
SEEDS = 30
SPEED_SD = 0.25     # how much responders differ in how fast they answer

# lognormal response time, tuned so P(>90s)=2% and P(>60s)=19%
MU, SIGMA = 3.79, 0.346

OLD = dict(wait=90, w_prox=0.45, w_acc=0.40, credit=0.08, decline=0.12,
           miss=0.12, decay=0.0)


def make_world(rng):
    resp = []
    for i in range(N_RESP):
        resp.append(dict(
            id=i,
            x=rng.uniform(0, 60), y=rng.uniform(0, 60),
            speed=math.exp(rng.gauss(0, SPEED_SD)),   # response-time multiplier
            turn_down=min(0.4, max(0.05, rng.gauss(0.21, 0.07))),
            score=0.5,
            pings=0, taken=0, missed=0,
        ))
    return resp


def proximity(r, cx, cy):
    minutes = math.hypot(r["x"] - cx, r["y"] - cy)  # 1 unit = 1 minute
    return 0.0 if minutes >= 45 else 1 - minutes / 45


def run_callout(resp, cfg, rng, stats):
    cx, cy = rng.uniform(0, 60), rng.uniform(0, 60)
    avail = [r for r in resp if rng.random() < P_AVAILABLE]
    # capability: each callout needs 1 of 3 tags; each responder has ~2 of 3
    need = rng.randrange(3)
    for r in avail:
        r["_cap"] = 1.0 if (hash((r["id"], need)) % 3) != 0 else 0.0
    ranked = sorted(
        avail,
        key=lambda r: (cfg["w_prox"] * proximity(r, cx, cy)
                       + cfg["w_acc"] * r["score"]
                       + 0.15 * r["_cap"]),
        reverse=True)
    elapsed = 0.0
    stats["callouts"] += 1
    for r in ranked:
        rt = math.exp(rng.gauss(MU, SIGMA)) * r["speed"]
        r["pings"] += 1
        stats["pings"] += 1
        if rt > cfg["wait"]:
            r["missed"] += 1
            stats["missed"] += 1
            elapsed += cfg["wait"]
            r["score"] -= cfg["miss"]
        elif rng.random() < r["turn_down"]:
            elapsed += rt
            r["score"] -= cfg["decline"]
        else:
            elapsed += rt
            r["taken"] += 1
            stats["taken"] += 1
            r["score"] += cfg["credit"]
            stats["delay"].append(elapsed)
            r["score"] = max(0.0, min(1.0, r["score"]))
            return
        r["score"] = max(0.0, min(1.0, r["score"]))
    stats["uncovered"] += 1


def run(cfg, seed):
    rng = random.Random(seed)
    resp = make_world(rng)
    # warm-up on old settings
    for _ in range(WARM_WEEKS):
        week(resp, OLD, rng, dict(callouts=0, pings=0, missed=0, taken=0,
                                  uncovered=0, delay=[]))
    for r in resp:
        r["pings"] = r["taken"] = r["missed"] = 0
    early = fresh()
    late = fresh()
    for w in range(TEST_WEEKS):
        week(resp, cfg, rng, early if w < 2 else (late if w >= TEST_WEEKS - 2 else fresh()))
    return resp, early, late


def fresh():
    return dict(callouts=0, pings=0, missed=0, taken=0, uncovered=0, delay=[])


def week(resp, cfg, rng, stats):
    for _ in range(CALLOUTS_PER_WEEK):
        run_callout(resp, cfg, rng, stats)
    if cfg["decay"]:
        for r in resp:
            r["score"] += (0.5 - r["score"]) * cfg["decay"]


def summarize(cfg):
    rows = []
    for seed in range(SEEDS):
        resp, early, late = run(cfg, seed)
        pings = sorted(r["pings"] for r in resp)
        total = sum(pings) or 1
        bottom4 = sum(pings[:4]) / total
        rows.append(dict(
            miss=late["missed"] / max(1, late["pings"]),
            ppc=late["pings"] / max(1, late["callouts"]),
            unc=late["uncovered"] / max(1, late["callouts"]),
            delay=st.median(late["delay"]) if late["delay"] else float("nan"),
            bottom4=bottom4,
            fewest=pings[0] / TEST_WEEKS,
        ))
    return {k: st.mean(r[k] for r in rows) for k in rows[0]}


def cfg(**kw):
    c = dict(OLD)
    c.update(kw)
    return c


SCENARIOS = [
    ("A  Before 4.2 (90s, 0.45/0.40)", cfg()),
    ("B  Today (60s, 0.60/0.25)", cfg(wait=60, w_prox=0.60, w_acc=0.25)),
    ("C  Restore 90s only", cfg(wait=90, w_prox=0.60, w_acc=0.25)),
    ("D  Restore weights only", cfg(wait=60)),
    ("E  Today + miss costs less (0.04)", cfg(wait=60, w_prox=0.60, w_acc=0.25, miss=0.04)),
    ("F  90s + miss costs less (0.04)", cfg(wait=90, w_prox=0.60, w_acc=0.25, miss=0.04)),
    ("G  F + score eases to neutral (5%/wk)", cfg(wait=90, w_prox=0.60, w_acc=0.25, miss=0.04, decay=0.05)),
    ("H  Today + ease to neutral only", cfg(wait=60, w_prox=0.60, w_acc=0.25, decay=0.05)),
    ("I  75s + miss 0.04 + ease", cfg(wait=75, w_prox=0.60, w_acc=0.25, miss=0.04, decay=0.05)),
    ("J  Misses cost nothing (0.00), 90s", cfg(wait=90, w_prox=0.60, w_acc=0.25, miss=0.0)),
]

SWEEP = [(f"prox {p:.2f} / acc {0.85 - p:.2f}",
          cfg(wait=90, w_prox=p, w_acc=0.85 - p, miss=0.04, decay=0.05))
         for p in (0.30, 0.45, 0.60, 0.75, 0.85)]


def table(title, items):
    print(f"\n{title}")
    print(f"{'scenario':<42}{'miss%':>7}{'pings/c':>9}{'unc%':>7}{'delay s':>9}{'bot4 %':>8}{'min p/wk':>9}")
    for name, c in items:
        s = summarize(c)
        print(f"{name:<42}{s['miss']*100:>7.1f}{s['ppc']:>9.2f}{s['unc']*100:>7.1f}"
              f"{s['delay']:>9.0f}{s['bottom4']*100:>8.1f}{s['fewest']:>9.1f}")


if __name__ == "__main__":
    print(f"{SEEDS} runs per scenario, {WARM_WEEKS} warm-up weeks then {TEST_WEEKS} test weeks; "
          "results are the last 2 weeks.")
    table("Settings scenarios", SCENARIOS)
    table("Proximity vs acceptance weight (90s, miss 0.04, ease 5%/wk)", SWEEP)
    SPEED_SD = 0.5
    table("Sensitivity: responders differ a lot in answer speed (sd 0.5)", [SCENARIOS[i] for i in (0, 1, 2, 5, 6, 8)])

#!/usr/bin/env python3
"""Poll-of-polls and seat forecast for the 7 November 2026 New Zealand general election.

    python3 tools/forecast.py                 # writes data/forecast.json
    python3 tools/forecast.py --asof 2026-10-01 --draws 5000 --out /tmp/f.json

Method (details and literature in guide/forecast-method.md):
  1. Poll aggregation - a per-party latent trend estimated by exponentially-weighted (half-life 21 days) pooling of
     house-effect-adjusted polls, weighted by sqrt(sample size). House effects = each pollster's mean deviation from the
     pooled trend over the whole term, constrained to sum to zero across the independent public pollsters
     (Jackman 2005; Linzer 2013; Ellis 2017/2020 for New Zealand).
  2. Error calibration - the final-three-weeks pooled polls of 2011-2023 vs the official results give the empirical
     error SD as a function of party size and the correlation of errors between parties (Jennings & Wlezien 2018;
     Shirani-Mehr et al. 2018).
  3. Monte Carlo - correlated party-vote draws around the aggregate (variance = calibrated error + random-walk drift for
     the days left), electorate draws for Epsom and the seven Maori seats, then the 5%/one-seat threshold and
     Sainte-Lague allocation (120 seats + overhang) for every draw.
  4. Backtest - the same aggregator run two weeks out on each election since 2011.
Pure Python + numpy; deterministic (fixed seed) so re-running on unchanged data gives identical output.
"""
import argparse, datetime as dt, json, math, os, sys
from collections import Counter, defaultdict
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
POLLS_2026 = os.path.join(ROOT, "data", "polls-2026.json")
HIST_DIR = os.path.join(ROOT, "data", "polls-history")
OUT = os.path.join(ROOT, "data", "forecast.json")
ELECTION_DAY = dt.date(2026, 11, 7)
PARTIES = ["national", "labour", "green", "act", "nz-first", "te-pati-maori", "opportunity"]
NAMES = {"national": "National", "labour": "Labour", "green": "Green", "act": "ACT", "nz-first": "NZ First",
         "te-pati-maori": "Te Pāti Māori", "opportunity": "Opportunity (TOP)", "te-tai-tokerau-party": "Te Tai Tokerau Party",
         "independent": "Independent", "others": "Others"}
HALF_LIFE_DAYS = 21.0
INTERNAL_WEIGHT = 0.5          # party/corporate-client polls published selectively: half weight, never anchor house effects
MIN_POLLS_FOR_HOUSE = 3
THRESHOLD = 5.0
MAORI_SEATS = ["Hauraki-Waikato", "Ikaroa-Rāwhiti", "Tāmaki Makaurau", "Te Tai Hauāuru", "Te Tai Tokerau", "Te Tai Tonga", "Waiariki"]
ELECTORATE_POLL_SYSTEMATIC_SD = 9.0   # points: electorate polls (n≈500, Maori roll hard to sample) miss by far more than sampling error
ELECTORATE_PRIOR_WEIGHT = 0.3         # weight on the 2023 result (same party's candidate) vs 0.7 on the 2026 electorate polls
ELECTIONS_2023 = os.path.join(ROOT, "data", "elections", "2023.json")
# 2023 winners who have since left Te Pati Maori: half of their 2023 vote is treated as personal (follows the candidate), half as party
PRIOR_SPLIT = {"Te Tai Tokerau": ("te-pati-maori", "te-tai-tokerau-party"), "Te Tai Tonga": ("te-pati-maori", "independent")}
HIST_ELECTIONS = {2011: "2011-11-26", 2014: "2014-09-20", 2017: "2017-09-23", 2020: "2020-10-17", 2023: "2023-10-14"}
GOVT_LEAD_PARTY = {2011: "national", 2014: "national", 2017: "national", 2020: "labour", 2023: "labour", 2026: "national"}


def d(s):
    return dt.date.fromisoformat(s[:10])


def load_polls(path):
    j = json.load(open(path, encoding="utf-8"))
    rows = []
    for p in j["polls"]:
        if p.get("is_election_result") or not p.get("end_date"):
            continue
        rows.append({"date": d(p["end_date"]), "pollster": p.get("pollster_key") or p["pollster"], "label": p["pollster"],
                     "n": p.get("sample_size") or None, "internal": bool(p.get("internal")), "results": dict(p["results"]),
                     "source_url": p.get("source_url"), "fieldwork": p.get("date")})
    rows.sort(key=lambda r: r["date"])
    return j, rows


# ----------------------------------------------------------------------------------------------------------------------
# 1. Aggregation
# ----------------------------------------------------------------------------------------------------------------------
def poll_weight(r, asof, half_life=HALF_LIFE_DAYS):
    age = (asof - r["date"]).days
    if age < 0:
        return 0.0
    w = math.exp(-math.log(2) * age / half_life)
    w *= math.sqrt((r["n"] or 1000) / 1000.0)
    if r["internal"]:
        w *= INTERNAL_WEIGHT
    return w


def weighted_level(rows, party, asof, house, half_life=HALF_LIFE_DAYS, window_days=120):
    """One-sided exponentially weighted mean of house-adjusted poll values for `party` at `asof`."""
    num = den = 0.0
    for r in rows:
        if party not in r["results"] or r["date"] > asof or (asof - r["date"]).days > window_days:
            continue
        w = poll_weight(r, asof, half_life)
        if w <= 0:
            continue
        num += w * (r["results"][party] - house.get(r["pollster"], {}).get(party, 0.0))
        den += w
    return (num / den) if den > 0 else None


def estimate_house_effects(rows, parties, asof, anchor, iters=5, half_life=HALF_LIFE_DAYS):
    """House effect = pollster's mean deviation from the pooled trend (iterated), sum-to-zero over `anchor` pollsters."""
    house = defaultdict(dict)
    for _ in range(iters):
        dev = defaultdict(lambda: defaultdict(list))
        for r in rows:
            if r["date"] > asof:
                continue
            for p in parties:
                if p not in r["results"]:
                    continue
                # trend at the poll's own date, using polls up to that date (incl. itself) - a one-sided local level
                lvl = weighted_level(rows, p, r["date"], house, half_life)
                if lvl is not None:
                    dev[r["pollster"]][p].append(r["results"][p] - lvl)
        new = defaultdict(dict)
        for ps, byp in dev.items():
            for p, ds in byp.items():
                n = len(ds)
                if n >= MIN_POLLS_FOR_HOUSE:
                    new[ps][p] = (sum(ds) / n) * n / (n + 2.0)     # mild shrinkage toward zero for short series
        # sum-to-zero over anchor pollsters (weighted by poll count): the public series define "the average pollster"
        for p in parties:
            a = [(ps, new[ps][p], len(dev[ps][p])) for ps in anchor if p in new.get(ps, {})]
            if a:
                mean = sum(h * n for _, h, n in a) / sum(n for _, _, n in a)
                for ps in new:
                    if p in new[ps]:
                        new[ps][p] -= mean
        house = new
    counts = {ps: len(next(iter(byp.values()))) for ps, byp in dev.items() if byp}
    return house, counts


def aggregate(rows, parties, asof, anchor, half_life=HALF_LIFE_DAYS, house=None):
    """Full aggregation at `asof`: estimate, standard error, house effects, residual noise, polls used."""
    if house is None:
        house, counts = estimate_house_effects(rows, parties, asof, anchor, half_life=half_life)
    else:
        counts = Counter(r["pollster"] for r in rows if r["date"] <= asof)
    out = {}
    for p in parties:
        est = weighted_level(rows, p, asof, house, half_life)
        if est is None:
            continue
        # residual dispersion of house-adjusted polls around the trend (beyond sampling error) over the last 120 days
        res, wsum, var_num = [], 0.0, 0.0
        for r in rows:
            if p not in r["results"] or r["date"] > asof or (asof - r["date"]).days > 120:
                continue
            w = poll_weight(r, asof, half_life)
            if w <= 0:
                continue
            lvl = weighted_level(rows, p, r["date"], house, half_life)
            adj = r["results"][p] - house.get(r["pollster"], {}).get(p, 0.0)
            res.append((w, adj - lvl))
        n_polls = len(res)
        tot_w = sum(w for w, _ in res) or 1.0
        rms = math.sqrt(sum(w * e * e for w, e in res) / tot_w) if res else 1.5
        # standard error of the weighted mean: each poll carries sampling variance + idiosyncratic variance (rms^2)
        var = 0.0
        for r in rows:
            if p not in r["results"] or r["date"] > asof or (asof - r["date"]).days > 120:
                continue
            w = poll_weight(r, asof, half_life)
            n = r["n"] or 1000
            samp = max(est, 0.5) * (100 - max(est, 0.5)) / n
            var += (w / tot_w) ** 2 * (samp + rms ** 2)
        out[p] = {"estimate": est, "se": math.sqrt(var) if var > 0 else 1.0, "n_polls_120d": n_polls, "poll_noise_sd": rms}
    return out, house, counts


# ----------------------------------------------------------------------------------------------------------------------
# 2. Calibration against 2011-2023
# ----------------------------------------------------------------------------------------------------------------------
def load_history():
    hist = {}
    for y, ed in HIST_ELECTIONS.items():
        path = os.path.join(HIST_DIR, f"{y}.json")
        if not os.path.exists(path):
            continue
        j, rows = load_polls(path)
        hist[y] = {"election": d(ed), "result": j.get("result") or {}, "rows": rows,
                   "anchor": sorted({r["pollster"] for r in rows if not r["internal"] and "election result" not in r["pollster"].lower()})}
    return hist


def final_weeks_average(rows, party, election, weeks=3):
    vals = [(math.sqrt((r["n"] or 1000) / 1000.0), r["results"][party]) for r in rows
            if party in r["results"] and 0 <= (election - r["date"]).days <= 7 * weeks]
    if len(vals) < 2:
        return None, len(vals)
    return sum(w * v for w, v in vals) / sum(w for w, _ in vals), len(vals)


def size_sd(p, k, floor=0.6):
    """Error SD as a function of party size: k * sqrt(p(100-p))/10 (binomial-shaped), with a floor for tiny parties."""
    p = min(max(p, 0.3), 99.7)
    return max(k * math.sqrt(p * (100 - p)) / 10.0, floor)


def calibrate(hist, exclude_year=None):
    """Final-3-weeks pooled average vs result -> per-party bias, size-dependent SD and inter-party error correlation."""
    errors = []    # (year, party, poll_avg, result, error)
    for y, h in hist.items():
        if y == exclude_year or not h["result"]:
            continue
        for party, actual in h["result"].items():
            if actual is None or party == "others":
                continue
            avg, n = final_weeks_average(h["rows"], party, h["election"])
            if avg is None or (avg < 0.5 and actual < 0.5):
                continue
            errors.append({"year": y, "party": party, "polls": avg, "result": actual, "error": actual - avg, "n_polls": n})
    # fit k in sd(p) = k*sqrt(p(100-p))/10 by least squares on squared errors (RMSE form -> absorbs bias into spread)
    num = sum(e["error"] ** 2 for e in errors)
    den = sum(((math.sqrt(e["polls"] * (100 - e["polls"])) / 10.0) ** 2) for e in errors)
    k = math.sqrt(num / den) if den else 0.5
    bins = {"major (>=20%)": lambda p: p >= 20, "mid (5-20%)": lambda p: 5 <= p < 20, "minor (<5%)": lambda p: p < 5}
    by_bin = {}
    for name, f in bins.items():
        es = [e for e in errors if f(e["polls"])]
        if es:
            by_bin[name] = {"n": len(es), "rmse": math.sqrt(sum(e["error"] ** 2 for e in es) / len(es)),
                            "mean_abs_error": sum(abs(e["error"]) for e in es) / len(es),
                            "mean_bias_result_minus_polls": sum(e["error"] for e in es) / len(es),
                            "model_sd_at_bin_mean": size_sd(sum(e["polls"] for e in es) / len(es), k)}
    by_party = defaultdict(list)
    for e in errors:
        by_party[e["party"]].append(e)
    party_bias = {p: {"n_elections": len(es), "mean_error_result_minus_polls": sum(e["error"] for e in es) / len(es),
                      "mean_abs_error": sum(abs(e["error"]) for e in es) / len(es),
                      "years_overstated_by_polls": [e["year"] for e in es if e["error"] < 0],
                      "years_understated_by_polls": [e["year"] for e in es if e["error"] > 0]}
                  for p, es in by_party.items() if len(es) >= 2}
    # inter-party correlation of errors (years x parties), pairwise over shared years, shrunk toward 0 (n is tiny)
    core = [p for p in PARTIES if sum(1 for e in errors if e["party"] == p) >= 3]
    years = sorted({e["year"] for e in errors})
    E = {(e["year"], e["party"]): e["error"] for e in errors}
    corr = {}
    for a in core:
        for b in core:
            ys = [y for y in years if (y, a) in E and (y, b) in E]
            if a == b or len(ys) < 4:
                corr[(a, b)] = 1.0 if a == b else 0.0
                continue
            xa = np.array([E[(y, a)] for y in ys]); xb = np.array([E[(y, b)] for y in ys])
            if xa.std() == 0 or xb.std() == 0:
                corr[(a, b)] = 0.0
                continue
            r = float(np.corrcoef(xa, xb)[0, 1])
            corr[(a, b)] = r * len(ys) / (len(ys) + 3.0)   # shrinkage: 5 elections cannot pin down a correlation
    return {"k": k, "errors": errors, "by_bin": by_bin, "party_bias": party_bias, "corr": corr, "core": core, "years": years}


def correlation_matrix(parties, corr, core):
    R = np.eye(len(parties))
    for i, a in enumerate(parties):
        for j, b in enumerate(parties):
            if i != j and a in core and b in core:
                R[i, j] = corr.get((a, b), 0.0)
    # make positive semi-definite
    w, v = np.linalg.eigh(R)
    w = np.clip(w, 0.05, None)
    R = v @ np.diag(w) @ v.T
    dg = np.sqrt(np.diag(R))
    return R / np.outer(dg, dg)


def drift_variance_per_day(trend, parties):
    """Random-walk innovation variance per day from week-to-week changes of the 2026 trend, scaled by party size."""
    out = {}
    for p in parties:
        xs = [t[p] for t in trend if t.get(p) is not None]
        if len(xs) < 10:
            out[p] = 0.01
            continue
        diffs = np.diff(np.array(xs))
        # weekly change variance minus the part that is just estimation noise is hard to separate with few polls;
        # use half the raw weekly variance as the innovation variance (the rest is poll noise) - conservative middle ground
        out[p] = max(float(np.var(diffs)) * 0.5 / 7.0, 0.002)
    return out


# ----------------------------------------------------------------------------------------------------------------------
# 3. Electorates + Sainte-Lague
# ----------------------------------------------------------------------------------------------------------------------
def sainte_lague(votes, seats):
    """votes: dict party->vote share (eligible parties only). Returns dict party->seats."""
    alloc = {p: 0 for p in votes}
    if seats <= 0 or not votes:
        return alloc
    quot = [(v / 1.0, p) for p, v in votes.items() if v > 0]
    import heapq
    heap = [(-q, p) for q, p in quot]
    heapq.heapify(heap)
    for _ in range(seats):
        q, p = heapq.heappop(heap)
        alloc[p] += 1
        heapq.heappush(heap, (-(votes[p] / (2 * alloc[p] + 1)), p))
    return alloc


def prior_shares_2023():
    """2023 candidate-vote shares by party in each Maori seat (data/elections/2023.json), used as a weak prior."""
    out = {}
    if not os.path.exists(ELECTIONS_2023):
        return out
    e = json.load(open(ELECTIONS_2023, encoding="utf-8"))
    for el in e.get("electorates", []):
        if el.get("name") in MAORI_SEATS and el.get("candidates"):
            tot = sum(c.get("votes") or 0 for c in el["candidates"]) or 1
            out[el["name"]] = {c["party"]: 100.0 * (c.get("votes") or 0) / tot for c in el["candidates"] if c.get("party")}
    for seat, (old, new) in PRIOR_SPLIT.items():
        if seat in out and old in out[seat]:
            half = out[seat][old] / 2
            out[seat][old], out[seat][new] = half, half
    return out


def electorate_assumptions(polls_json, rng, n_draws):
    """Per-seat win probabilities for the seats that can change the seat allocation, simulated from electorate polls.

    Decided-voter shares = 0.7 x mean of the electorate polls in the last 45 days + 0.3 x the same party's 2023 share
    (new candidates/parties get a zero prior, so the polls carry them). Each candidate is drawn with
    SD = sqrt(sampling + ELECTORATE_POLL_SYSTEMATIC_SD^2); the highest draw wins."""
    eps = [e for e in polls_json.get("electorate_polls", []) if e.get("vote") == "electorate"]
    prior = prior_shares_2023()
    seats = {}
    for seat in MAORI_SEATS:
        rows = sorted([e for e in eps if e["electorate"] == seat and e.get("end_date")], key=lambda e: e["end_date"], reverse=True)
        if not rows:
            continue
        latest = d(rows[0]["end_date"])
        use = [e for e in rows if (latest - d(e["end_date"])).days <= 45]
        cands = sorted({c for e in use for c in e["results"]})
        poll_mean = {c: float(np.mean([e["results"].get(c, 0.0) for e in use])) for c in cands}
        tot = sum(poll_mean.values()) or 1.0
        poll_share = {c: poll_mean[c] * 100 / tot for c in cands}
        pr = {c: prior.get(seat, {}).get(c, 0.0) for c in cands}
        ptot = sum(pr.values())
        pr = {c: (v * 100 / ptot if ptot else poll_share[c]) for c, v in pr.items()}
        blend = {c: (1 - ELECTORATE_PRIOR_WEIGHT) * poll_share[c] + ELECTORATE_PRIOR_WEIGHT * pr[c] for c in cands}
        n_eff = sum(e.get("sample_size") or 500 for e in use)
        seats[seat] = {"shares": blend, "poll_shares": poll_share, "prior_2023": pr, "n_eff": n_eff,
                       "polls": [{"pollster": e["pollster"], "date": e["date"], "sample_size": e.get("sample_size"), "results": e["results"], "source_url": e.get("source_url")} for e in use]}
    winners, probs = {}, {}
    for seat, s in seats.items():
        cands = list(s["shares"])
        mu = np.array([s["shares"][c] for c in cands])
        samp_sd = np.sqrt(np.clip(mu, 1, 99) * (100 - np.clip(mu, 1, 99)) / s["n_eff"])
        sd = np.sqrt(samp_sd ** 2 + ELECTORATE_POLL_SYSTEMATIC_SD ** 2)
        draws = mu + rng.standard_normal((n_draws, len(cands))) * sd
        idx = np.argmax(draws, axis=1)
        winners[seat] = np.array(cands)[idx]
        probs[seat] = {c: float(np.mean(idx == i)) for i, c in enumerate(cands)}
    return seats, probs, winners


# ----------------------------------------------------------------------------------------------------------------------
# 4. Simulation
# ----------------------------------------------------------------------------------------------------------------------
def simulate(mean, sd, R, parties, polls_json, n_draws, rng, p_epsom_act=0.90, ttt_party_vote=0.3):
    k = len(parties)
    L = np.linalg.cholesky(R)
    z = rng.standard_normal((n_draws, k)) @ L.T
    # logit-normal keeps small parties positive and skews their uncertainty upward, as observed for minor parties
    mu = np.array([mean[p] for p in parties]) / 100.0
    s = np.array([sd[p] for p in parties]) / 100.0
    logit = np.log(mu / (1 - mu))
    dlogit = s / (mu * (1 - mu))            # delta method: sd on the logit scale
    shares = 1 / (1 + np.exp(-(logit + z * dlogit))) * 100.0
    # keep the total of the listed parties below ~100 (others ~1-3%)
    tot = shares.sum(axis=1, keepdims=True)
    shares = np.where(tot > 99.0, shares * 99.0 / tot, shares)

    seat_info, seat_probs, seat_winners = electorate_assumptions(polls_json, rng, n_draws)
    epsom_act = rng.random(n_draws) < p_epsom_act
    seats_out = np.zeros((n_draws, k), dtype=int)
    extra = {"te-tai-tokerau-party": np.zeros(n_draws, dtype=int), "independent": np.zeros(n_draws, dtype=int)}
    totals = np.zeros(n_draws, dtype=int)
    pidx = {p: i for i, p in enumerate(parties)}
    for i in range(n_draws):
        elect = Counter()
        if epsom_act[i]:
            elect["act"] += 1
        for seat, w in seat_winners.items():
            elect[str(w[i])] += 1
        # general electorates: National/Labour/Green win many, but never more than their list entitlement (assumption)
        votes = {p: shares[i, j] for j, p in enumerate(parties)}
        ind = elect.get("independent", 0)
        eligible = {p: v for p, v in votes.items() if v >= THRESHOLD or elect.get(p, 0) > 0}
        if elect.get("te-tai-tokerau-party", 0) > 0:
            eligible["te-tai-tokerau-party"] = ttt_party_vote
        alloc = sainte_lague(eligible, 120 - ind)
        row = {}
        for p in eligible:
            row[p] = max(alloc.get(p, 0), elect.get(p, 0))
        for p in parties:
            seats_out[i, pidx[p]] = row.get(p, 0)
        extra["te-tai-tokerau-party"][i] = row.get("te-tai-tokerau-party", 0)
        extra["independent"][i] = ind
        totals[i] = sum(row.values()) + ind
    return shares, seats_out, extra, totals, seat_info, seat_probs, epsom_act


def pct(x):
    return int(round(100 * float(x)))


def q(a, lo, hi):
    return [float(np.quantile(a, lo)), float(np.quantile(a, hi))]


# ----------------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", default=None, help="pretend today is this date (YYYY-MM-DD)")
    ap.add_argument("--draws", type=int, default=40000)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--seed", type=int, default=20261107)
    args = ap.parse_args()
    asof = d(args.asof) if args.asof else dt.date.today()
    if asof > ELECTION_DAY:
        asof = ELECTION_DAY
    days_left = (ELECTION_DAY - asof).days
    rng = np.random.default_rng(args.seed)

    polls_json, rows = load_polls(POLLS_2026)
    rows = [r for r in rows if r["date"] <= asof]
    anchor = sorted({r["pollster"] for r in rows if not r["internal"]})
    agg, house, counts = aggregate(rows, PARTIES, asof, anchor)

    # weekly trend (one-sided, house effects held at the full-term estimate)
    start = dt.date(2023, 10, 16)
    trend = []
    t = start
    while t <= asof:
        pt = {"week_ending": t.isoformat()}
        for p in PARTIES:
            v = weighted_level(rows, p, t, house)
            pt[p] = round(v, 1) if v is not None else None
        if any(pt[p] is not None for p in PARTIES):
            trend.append(pt)
        t += dt.timedelta(days=7)
    if trend and trend[-1]["week_ending"] != asof.isoformat():
        pt = {"week_ending": asof.isoformat()}
        for p in PARTIES:
            pt[p] = round(agg[p]["estimate"], 1) if p in agg else None
        trend.append(pt)

    # calibration + drift
    hist = load_history()
    cal = calibrate(hist)
    R = correlation_matrix(PARTIES, cal["corr"], cal["core"])
    drift = drift_variance_per_day(trend, PARTIES)
    mean, sd, sd_parts = {}, {}, {}
    for p in PARTIES:
        est = agg[p]["estimate"]
        cal_sd = size_sd(est, cal["k"])
        agg_se = agg[p]["se"]
        drift_sd = math.sqrt(drift[p] * max(days_left, 0))
        total = math.sqrt(cal_sd ** 2 + agg_se ** 2 + drift_sd ** 2)
        mean[p], sd[p] = est, total
        sd_parts[p] = {"calibrated_poll_error_sd": round(cal_sd, 2), "aggregate_se": round(agg_se, 2), "drift_sd_to_election": round(drift_sd, 2), "total_sd": round(total, 2)}

    shares, seats, extra, totals, seat_info, seat_probs, epsom_act = simulate(mean, sd, R, PARTIES, polls_json, args.draws, rng)
    pidx = {p: i for i, p in enumerate(PARTIES)}
    tot_seats = totals
    maj = tot_seats // 2 + 1
    blocs = {
        "National + ACT + NZ First": ["national", "act", "nz-first"],
        "Labour + Green + Te Pāti Māori": ["labour", "green", "te-pati-maori"],
        "Labour + Green + Te Pāti Māori + TOP": ["labour", "green", "te-pati-maori", "opportunity"],
        "National + ACT + NZ First + TOP": ["national", "act", "nz-first", "opportunity"],
        "National + ACT": ["national", "act"],
        "Labour + Green": ["labour", "green"],
        "Labour + Green + TOP": ["labour", "green", "opportunity"],
        "Labour + NZ First": ["labour", "nz-first"],
        "National + NZ First": ["national", "nz-first"],
    }
    bloc_seats = {name: seats[:, [pidx[p] for p in ps]].sum(axis=1) for name, ps in blocs.items()}
    right = bloc_seats["National + ACT + NZ First"]; left = bloc_seats["Labour + Green + Te Pāti Māori"]
    right_maj, left_maj = right >= maj, left >= maj
    no_maj = ~right_maj & ~left_maj
    top_seats = seats[:, pidx["opportunity"]]
    top_kingmaker = no_maj & ((right + top_seats >= maj) | (left + top_seats >= maj))
    nzf_seats = seats[:, pidx["nz-first"]]
    nzf_kingmaker = ~(bloc_seats["National + ACT"] >= maj) & ~left_maj & ((bloc_seats["National + ACT"] + nzf_seats >= maj) | (bloc_seats["Labour + Green"] + nzf_seats >= maj))

    def hist_of(a):
        c = Counter(int(x) for x in a)
        return {str(k): pct(v / len(a)) for k, v in sorted(c.items()) if round(100 * v / len(a)) >= 1}

    # most likely parliament = modal seat vector
    mode_key, mode_n = Counter(tuple(int(x) for x in r) for r in seats).most_common(1)[0]

    # latest poll per pollster + house effects table
    latest = {}
    for r in rows:
        if r["pollster"] not in latest or r["date"] > latest[r["pollster"]]["date"]:
            latest[r["pollster"]] = r
    pollsters_out = []
    for ps in sorted(latest, key=lambda s: latest[s]["date"], reverse=True):
        meta = polls_json.get("pollsters", {}).get(ps, {})
        pollsters_out.append({"pollster": ps, "type": meta.get("type"), "commissioner": meta.get("commissioner"), "internal": latest[ps]["internal"],
                              "n_polls_this_term": counts.get(ps, 0), "anchor_for_house_effects": ps in anchor,
                              "house_effects": {p: round(house.get(ps, {}).get(p, 0.0), 1) for p in PARTIES if p in house.get(ps, {})},
                              "latest_poll": {"fieldwork": latest[ps]["fieldwork"], "end_date": latest[ps]["date"].isoformat(), "sample_size": latest[ps]["n"],
                                              "results": latest[ps]["results"], "source_url": latest[ps]["source_url"]}})

    # ---- backtest: aggregator two weeks out, leave-one-year-out calibration ----
    backtest = []
    for y, h in sorted(hist.items()):
        if not h["result"]:
            continue
        cal_y = calibrate(hist, exclude_year=y)
        two_weeks = h["election"] - dt.timedelta(days=14)
        hrows = [r for r in h["rows"] if r["date"] <= two_weeks and r["date"] > h["election"] - dt.timedelta(days=3 * 365)]
        parties_y = [p for p in h["result"] if p != "others" and sum(1 for r in hrows if p in r["results"] and (two_weeks - r["date"]).days <= 120) >= 3]
        agg_y, house_y, _ = aggregate(hrows, parties_y, two_weeks, h["anchor"])
        tbl, inside80, inside95, n = [], 0, 0, 0
        for p in parties_y:
            if p not in agg_y:
                continue
            est = agg_y[p]["estimate"]; actual = h["result"][p]
            sdp = math.sqrt(size_sd(est, cal_y["k"]) ** 2 + agg_y[p]["se"] ** 2)
            lo80, hi80 = est - 1.2816 * sdp, est + 1.2816 * sdp
            lo95, hi95 = est - 1.96 * sdp, est + 1.96 * sdp
            in80, in95 = lo80 <= actual <= hi80, lo95 <= actual <= hi95
            if actual >= 1.0 or est >= 1.0:
                n += 1; inside80 += in80; inside95 += in95
            tbl.append({"party": p, "forecast_2wk_out": round(est, 1), "sd": round(sdp, 1), "interval80": [round(lo80, 1), round(hi80, 1)],
                        "result": actual, "error_result_minus_forecast": round(actual - est, 1), "inside80": bool(in80), "inside95": bool(in95)})
        final3 = {}
        for p in parties_y:
            avg, npolls = final_weeks_average(h["rows"], p, h["election"])
            if avg is not None:
                final3[p] = {"final3wk_avg": round(avg, 1), "result": h["result"][p], "error": round(h["result"][p] - avg, 1), "n_polls": npolls}
        mid = h["election"] - dt.timedelta(days=540)
        gov = GOVT_LEAD_PARTY[y]
        mid_lvl = weighted_level([r for r in h["rows"] if r["date"] <= mid], gov, mid, {}, HALF_LIFE_DAYS, window_days=120)
        backtest.append({"election": y, "election_date": h["election"].isoformat(), "forecast_date": two_weeks.isoformat(),
                         "n_polls_used_120d": sum(1 for r in hrows if (two_weeks - r["date"]).days <= 120),
                         "pollsters": sorted({r["pollster"] for r in hrows if (two_weeks - r["date"]).days <= 120}),
                         "parties": tbl, "coverage80": f"{inside80}/{n}", "coverage95": f"{inside95}/{n}",
                         "mean_abs_error_major_parties": round(float(np.mean([abs(t["error_result_minus_forecast"]) for t in tbl if t["result"] >= 5])), 1) if tbl else None,
                         "final_3_weeks_vs_result": final3,
                         "incumbent_government_lead_party": gov,
                         "incumbent_midterm_poll_level": round(mid_lvl, 1) if mid_lvl is not None else None,
                         "incumbent_midterm_date": mid.isoformat(),
                         "incumbent_result": h["result"].get(gov),
                         "incumbent_change_midterm_to_result": round(h["result"][gov] - mid_lvl, 1) if mid_lvl is not None and gov in h["result"] else None})
    cov80 = sum(int(b["coverage80"].split("/")[0]) for b in backtest); cov80n = sum(int(b["coverage80"].split("/")[1]) for b in backtest)
    cov95 = sum(int(b["coverage95"].split("/")[0]) for b in backtest); cov95n = sum(int(b["coverage95"].split("/")[1]) for b in backtest)

    # 2026 incumbent mid-term comparison
    mid26 = ELECTION_DAY - dt.timedelta(days=540)
    mid26_lvl = weighted_level([r for r in rows if r["date"] <= mid26], "national", mid26, house)

    # ---- assemble ----
    parties_out = []
    for p in PARTIES:
        i = pidx[p]
        parties_out.append({
            "party": p, "name": NAMES[p],
            "poll_average": round(mean[p], 1),
            "poll_average_80": [round(mean[p] - 1.2816 * agg[p]["se"], 1), round(mean[p] + 1.2816 * agg[p]["se"], 1)],
            "poll_average_95": [round(mean[p] - 1.96 * agg[p]["se"], 1), round(mean[p] + 1.96 * agg[p]["se"], 1)],
            "forecast_vote_mean": round(float(shares[:, i].mean()), 1),
            "forecast_vote_80": [round(x, 1) for x in q(shares[:, i], 0.10, 0.90)],
            "forecast_vote_95": [round(x, 1) for x in q(shares[:, i], 0.025, 0.975)],
            "uncertainty": sd_parts[p],
            "n_polls_last_120_days": agg[p]["n_polls_120d"],
            "seats_mean": round(float(seats[:, i].mean()), 1),
            "seats_expected": int(round(float(seats[:, i].mean()))),
            "seats_80": [int(x) for x in q(seats[:, i], 0.10, 0.90)],
            "seats_95": [int(x) for x in q(seats[:, i], 0.025, 0.975)],
            "seat_histogram": hist_of(seats[:, i]),
            "p_over_5pct": pct((shares[:, i] >= THRESHOLD).mean()),
            "p_wins_electorate": pct((seats[:, i] > 0).mean() if p in ("te-pati-maori",) else
                                     (epsom_act.mean() if p == "act" else (1.0 if p in ("national", "labour", "green") else 0.0))),
            "p_in_parliament": pct((seats[:, i] > 0).mean()),
            "p_largest_party": pct((shares[:, i] == shares.max(axis=1)).mean()),
        })
    others_seats = {k: {"seats_expected": int(round(float(v.mean()))), "p_wins_seat": pct((v > 0).mean()), "seat_histogram": hist_of(v)} for k, v in extra.items()}

    out = {
        "title": "Poll-of-polls and seat forecast: 2026 New Zealand general election",
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "as_of": asof.isoformat(), "election_date": ELECTION_DAY.isoformat(), "days_to_election": days_left,
        "polls_source": polls_json.get("source"), "polls_retrieved": polls_json.get("retrieved"),
        "n_polls_this_term": len(rows), "n_polls_last_120_days": sum(1 for r in rows if (asof - r["date"]).days <= 120),
        "latest_poll_date": max(r["date"] for r in rows).isoformat(),
        "method_doc": "guide/forecast-method.md",
        "how_to_read": [
            "The poll average is where the public polls, adjusted for each pollster's habitual lean, put each party today. Its interval shows only how noisy the polls are.",
            "The forecast interval is wider: it adds how far New Zealand's final polls have missed the result at the last five elections and how much support can still move before 7 November.",
            "Seats come from running the real MMP rules (5% or an electorate seat, Sainte-Laguë, overhang) on tens of thousands of simulated results. Expected seats are an average; the 80% range is where 8 in 10 simulations land.",
            "A bloc's 'majority' probability is the share of simulations in which those parties alone hold more than half of all seats, including overhang seats.",
            "Probabilities are rounded to the nearest 1% and seats to whole numbers deliberately: the inputs are not precise enough to justify more.",
            "A 70% chance is not a certainty: it means the other outcome happens about 3 times in 10.",
        ],
        "headline": {
            "largest_party_probability": {p: pct((shares[:, pidx[p]] == shares.max(axis=1)).mean()) for p in ("national", "labour")},
            "p_right_bloc_majority_NAT_ACT_NZF": pct(right_maj.mean()),
            "p_left_bloc_majority_LAB_GRN_TPM": pct(left_maj.mean()),
            "p_no_bloc_majority": pct(no_maj.mean()),
            "p_TOP_holds_balance_of_power": pct(top_kingmaker.mean()),
            "p_NZ_First_holds_balance_of_power": pct(nzf_kingmaker.mean()),
            "p_TOP_over_5pct": pct((shares[:, pidx["opportunity"]] >= THRESHOLD).mean()),
            "p_NZ_First_over_5pct": pct((shares[:, pidx["nz-first"]] >= THRESHOLD).mean()),
            "p_TPM_over_5pct": pct((shares[:, pidx["te-pati-maori"]] >= THRESHOLD).mean()),
            "p_overhang": pct((tot_seats > 120).mean()),
            "expected_total_seats": int(round(float(tot_seats.mean()))),
        },
        "parties": parties_out,
        "other_seat_winners": others_seats,
        "blocs": [{"bloc": name, "parties": ps, "seats_expected": int(round(float(bloc_seats[name].mean()))),
                   "seats_80": [int(x) for x in q(bloc_seats[name], 0.10, 0.90)],
                   "p_majority": pct((bloc_seats[name] >= maj).mean()), "seat_histogram": hist_of(bloc_seats[name])}
                  for name, ps in blocs.items()],
        "p_no_bloc_majority": pct(no_maj.mean()),
        "majority_threshold": {"usual": 61, "note": "61 of 120; one more for every two overhang seats (62 of 122-123)", "distribution_total_seats": hist_of(tot_seats)},
        "most_likely_parliament": {"seats": {p: mode_key[pidx[p]] for p in PARTIES}, "share_of_simulations": round(100 * mode_n / args.draws, 1),
                                   "note": "The single most frequent exact seat combination; even the most likely one occurs in only a few per cent of simulations."},
        "trend_weekly": trend,
        "pollsters": pollsters_out,
        "house_effects_note": ("House effect = that pollster's average deviation from the pooled trend this term, after shrinkage, in percentage points; "
                               "positive = the pollster runs high for that party. Constrained to average zero across the independent public pollsters "
                               f"({', '.join(anchor)}), so they describe relative leans, not absolute bias. Party-commissioned/corporate polls (internal=true) "
                               "get half weight and do not anchor the average."),
        "undecided_note": ("All NZ pollsters publish party shares with undecided voters (typically 5-15%) excluded, so polls already sum to ~100% of decided voters "
                           "and the aggregate is used as published. 'Others' are implied as 100 minus the seven listed parties. The historical calibration "
                           "measures the resulting error directly, so no separate undecided adjustment is applied."),
        "aggregation_settings": {"half_life_days": HALF_LIFE_DAYS, "sample_size_weight": "sqrt(n/1000)", "internal_poll_weight": INTERNAL_WEIGHT,
                                 "window_days": 120, "house_effect_min_polls": MIN_POLLS_FOR_HOUSE, "one_sided": True},
        "calibration": {
            "elections_used": cal["years"],
            "method": "Final-3-weeks pooled average (sqrt(n) weights, no house adjustment) vs official result, per party; "
                      "error SD modelled as k*sqrt(p(100-p))/10 fitted by least squares on squared errors (so historical bias widens the spread rather than shifting the mean).",
            "k": round(cal["k"], 3),
            "model_sd_examples": {str(p): round(size_sd(p, cal["k"]), 2) for p in (1, 3, 5, 10, 15, 30, 45)},
            "by_party_size": {k2: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k2, v in cal["by_bin"].items()},
            "by_party_bias": {p: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for p, v in cal["party_bias"].items()},
            "error_table": [{k2: (round(v, 2) if isinstance(v, float) else v) for k2, v in e.items()} for e in cal["errors"]],
            "correlation_used": {f"{a}|{b}": round(float(R[pidx[a], pidx[b]]), 2) for a in PARTIES for b in PARTIES if pidx[a] < pidx[b] and abs(R[pidx[a], pidx[b]]) >= 0.05},
            "correlation_note": "Pairwise correlation of final-poll errors across the five elections (pairs with at least four shared elections), shrunk by n/(n+3) because five observations cannot pin down a correlation; matrix forced positive-definite.",
            "drift_variance_per_day": {p: round(v, 4) for p, v in drift.items()},
            "drift_note": "Random-walk innovation variance per day, estimated from week-to-week changes in this term's own trend (half attributed to real movement). Multiplied by days to the election.",
        },
        "electorates": {
            "note": ("Only electorates that can change the seat allocation are simulated: Epsom (ACT's insurance seat) and the seven Māori seats "
                     "(Te Pāti Māori's party vote is far below 5%, so every seat it wins is an overhang seat; an independent or Te Tai Tokerau Party winner also changes the arithmetic). "
                     "General seats won by National, Labour or the Greens are assumed never to exceed those parties' list entitlement, so they do not affect totals."),
            "epsom": {"p_act_wins": pct(epsom_act.mean()), "assumption": ("David Seymour (ACT) won Epsom by 8,142 votes in 2023 over Paul Goldsmith (National), who is standing again; "
                                                                        "National has not formally stood aside but did not campaign hard for the seat in 2023. ACT is polling 9-11% so Epsom only matters if ACT fell below 5%. "
                                                                        "Set at 90% (no 2026 Epsom poll)."),
                      "sources": ["data/elections/2023.json", "https://www.1news.co.nz/2026/08/16/goldsmith-rules-out-kaipara-ki-mahurangi-run-will-stay-in-epsom/"]},
            "maori_seats": {seat: {"p_win": {c: pct(v) for c, v in sorted(seat_probs[seat].items(), key=lambda kv: -kv[1])},
                                   "shares_used": {c: round(v, 1) for c, v in seat_info[seat]["shares"].items()},
                                   "poll_shares_decided": {c: round(v, 1) for c, v in seat_info[seat]["poll_shares"].items()},
                                   "prior_2023_shares": {c: round(v, 1) for c, v in seat_info[seat]["prior_2023"].items()},
                                   "polls_used": seat_info[seat]["polls"],
                                   "simulation": f"shares_used = {1 - ELECTORATE_PRIOR_WEIGHT:.1f} x decided-voter shares from the electorate polls above (n_eff={seat_info[seat]['n_eff']}) + {ELECTORATE_PRIOR_WEIGHT:.1f} x the same party's 2023 candidate-vote share; each candidate drawn with SD = sqrt(sampling + {ELECTORATE_POLL_SYSTEMATIC_SD:.0f}^2) points; winner = highest draw."}
                            for seat in MAORI_SEATS if seat in seat_probs},
            "maori_seats_context": [
                "2023: Te Pāti Māori won 6 of 7 (Tāmaki Makaurau by 42 votes, Te Tai Tokerau by 517); Labour held Ikaroa-Rāwhiti.",
                "6 Sep 2025 Tāmaki Makaurau by-election: Oriini Kaipara (TPM) 6,948 beat Peeni Henare (Labour) 3,429 (turnout low). Kaipara stands again; Labour's candidate is Kerrin Leoni.",
                "Nov 2025: Tākuta Ferris (Te Tai Tonga) and Mariameno Kapa-Kingi (Te Tai Tokerau) were expelled from TPM; Kapa-Kingi was reinstated by the High Court, then left in May 2026 to found Te Tai Tokerau Party. Ferris stands as an independent.",
                "Prior for Te Tai Tokerau and Te Tai Tonga: half of the 2023 Te Pāti Māori candidate vote is credited to the sitting MP's new vehicle (Te Tai Tokerau Party / independent) and half to Te Pāti Māori.",
                "Electorate polls in Māori seats have small samples (n≈500) and a history of large misses; the 9-point systematic error term and the 30% weight on the 2023 result reflect that.",
            ],
        },
        "historical_track_record": {
            "note": "What this model would have said two weeks before each election since 2011 (polls as of that date, house effects estimated from that term, calibration from the other four elections) versus the official result; plus the final-3-weeks simple pooled average, and how the governing party moved from mid-term (18 months out) to polling day.",
            "coverage80": f"{cov80}/{cov80n}", "coverage95": f"{cov95}/{cov95n}",
            "elections": backtest,
            "incumbent_2026": {"party": "national", "midterm_date": mid26.isoformat(), "midterm_poll_level": round(mid26_lvl, 1) if mid26_lvl is not None else None,
                               "current_poll_average": round(mean["national"], 1), "result_2023": 38.08},
        },
        "caveats": [
            "Polling error: at the last five elections NZ's final polls missed individual parties by up to 5 points (National 2020). The forecast intervals are built from those misses, but a miss bigger than any since 2011 is always possible.",
            "Threshold effects: TOP and NZ First sit near the 5% line, and Te Pāti Māori's seats depend on a handful of Māori-electorate contests. A one-point shift can move 6-10 seats between blocs, which is why the bloc probabilities are far less certain than the vote shares.",
            "Electorate assumptions: Epsom and the Māori seats are modelled from very few, small-sample electorate polls and stated assumptions; those probabilities are the model's weakest input.",
            "Late swing: a fifth of voters typically decide in the final fortnight; advance voting (which opened 26 Oct) blunts but does not remove this.",
            "Undecideds: polls exclude 5-15% undecided voters; if they break unevenly the published shares shift.",
            "House effects are relative to the average public pollster, not to the truth; if all pollsters share a bias (as in 2020) the aggregate shares it.",
            "Party-commissioned and corporate-client polls (Talbot Mills, Anacta, Curia) are published selectively and are down-weighted, but may still colour the average.",
            "The model does not forecast coalition negotiations: a 'majority' means the seats exist, not that the parties would agree to govern together.",
            "Only seven parties are modelled; a minor party winning an electorate or crossing 5% from nowhere is not simulated.",
        ],
        "sources": [
            polls_json.get("source"),
            "https://freerangestats.info/elections/state-space",
            "https://freerangestats.info/blog/2020/06/06/nz-2020-forecasts",
            "https://doi.org/10.1080/10361140500302472",
            "https://doi.org/10.1080/01621459.2012.737735",
            "https://doi.org/10.1038/s41562-018-0315-6",
            "https://doi.org/10.1080/01621459.2018.1448823",
            "https://www.1news.co.nz/2026/08/28/i-dont-believe-your-poll-politicians-like-to-say-but-are-they-right/",
            "https://elections.nz/democracy-in-nz/what-is-new-zealands-system-of-government/what-is-mmp/",
        ],
        "simulation": {"draws": args.draws, "seed": args.seed, "distribution": "multivariate logit-normal around the poll average"},
    }
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    h = out["headline"]
    print(f"as of {asof} ({days_left} days out): " + ", ".join(f"{NAMES[p]} {mean[p]:.1f}±{sd[p]:.1f}" for p in PARTIES))
    print(f"seats: " + ", ".join(f"{NAMES[p]} {po['seats_expected']} [{po['seats_80'][0]}-{po['seats_80'][1]}]" for p, po in zip(PARTIES, parties_out)))
    print(f"P(right maj) {h['p_right_bloc_majority_NAT_ACT_NZF']}%  P(left maj) {h['p_left_bloc_majority_LAB_GRN_TPM']}%  P(none) {h['p_no_bloc_majority']}%  "
          f"P(TOP kingmaker) {h['p_TOP_holds_balance_of_power']}%  P(TOP>5) {h['p_TOP_over_5pct']}%  P(overhang) {h['p_overhang']}%")
    print(f"backtest coverage 80%: {out['historical_track_record']['coverage80']}, 95%: {out['historical_track_record']['coverage95']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

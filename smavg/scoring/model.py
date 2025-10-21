from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import json, datetime, subprocess

@dataclass
class Metric:
    domain: str
    name: str
    score: float
    trust: str
    source: str

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def weighted_domain_scores(metrics: List[Metric], trust_weights: Dict[str, float]) -> Dict[str, float]:
    by = {}
    for m in metrics:
        w = trust_weights.get(m.trust, 0.0)
        if w <= 0:
            continue
        agg = by.setdefault(m.domain, {"num":0.0, "den":0.0})
        agg["num"] += m.score * w
        agg["den"] += w
    return {d:(v["num"]/v["den"] if v["den"]>0 else 0.0) for d,v in by.items()}

def aggregate_agi_percent(domain_means: Dict[str, float], domain_weights: Dict[str, float]) -> float:
    total = 0.0
    for d, w in domain_weights.items():
        total += w * domain_means.get(d, 0.0)
    return round(total * 100, 1)

def compute_time_bar_percent(cfg: dict) -> float:
    mode = cfg.get("mode", "median_date")
    if mode == "median_date":
        lower = int(cfg.get("lower_bound_year", 2020))
        median = int(cfg.get("median_year", 2034))
        year = datetime.date.today().year
        if median <= lower: return 0.0
        pct = (year - lower) / (median - lower)
        return float(max(0.0, min(1.0, pct)) * 100.0)
    elif mode == "progress_proxy":
        return float(max(0.0, min(100.0, cfg.get("progress", 0.0))))
    return 0.0

def get_git_commit() -> str:
    try:
        res = subprocess.run(["git","rev-parse","--short","HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def run_score(metrics_path="data/metrics.json", sources_path="data/sources.json"):
    mdata = load_json(metrics_path)
    sdata = load_json(sources_path)

    metrics = [Metric(**x) for x in mdata["metrics"]]
    trust_w = sdata["trust_weights"]
    dom_w   = sdata["domain_weights"]

    dom_means = weighted_domain_scores(metrics, trust_w)
    agi_pct   = aggregate_agi_percent(dom_means, dom_w)
    time_pct  = compute_time_bar_percent(sdata.get("time_bar", {}))

    state = {
        "as_of": mdata.get("as_of", datetime.datetime.utcnow().isoformat() + "+05:30"),
        "track": mdata.get("track", "pure_model"),
        "domain_means": dom_means,
        "agi_percent": agi_pct,
        "time_percent": round(time_pct, 1),
        "counts": {
            "metrics_total": len(metrics),
            "metrics_counted": sum(1 for x in metrics if trust_w.get(x.trust,0)>0)
        },
        "commit": get_git_commit()
    }
    with open("data/state.json","w",encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return state

if __name__ == "__main__":
    print(json.dumps(run_score(), indent=2))

"""Recompute every number in results/results.md from data/scores.csv.

Usage (from the repository root):
    python pipeline/analyze.py

Scores: K = kept, D = dropped, W = wrong, C = caveat lost.
A fact counts as kept only if scored K.
"""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["ChatGPT", "Gemini", "Claude"]
BASELINE = ["MMC-V0", "TSM", "PNC", "AA", "JPM"]
STEERING = ["MMC-V0", "MMC-V1", "MMC-V2", "MMC-V3"]
TARGET = "M7"  # the Marsh fact moved in the steering test


def load():
    with open(ROOT / "data" / "scores.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def kept(rows):
    n = len(rows)
    k = sum(r["score"] == "K" for r in rows)
    return f"{k}/{n} ({100 * k / n:.0f}%)" if n else "n/a"


def main():
    rows = load()
    base = [r for r in rows if r["file"] in BASELINE]
    assert len(base) == 150, "expected 5 calls x 3 models x 10 facts"

    print("Baseline: share of facts fully kept")
    for m in MODELS:
        sub = [r for r in base if r["model"] == m]
        c = Counter(r["score"] for r in sub)
        print(f"  {m:8} {kept(sub):12} dropped {c['D']}, caveat lost {c['C']}, wrong {c['W']}")
    print(f"  {'All':8} {kept(base)}")

    print("\nBaseline: prepared remarks (PR) vs. Q&A-only (QA)")
    for m in MODELS + ["All"]:
        sub = base if m == "All" else [r for r in base if r["model"] == m]
        pr = [r for r in sub if r["where"] == "PR"]
        qa = [r for r in sub if r["where"] == "QA"]
        print(f"  {m:8} PR {kept(pr):12} QA {kept(qa)}")

    print("\nBaseline: bad news vs. other facts")
    print(f"  bad news {kept([r for r in base if r['neg'] == 'Y'])}")
    print(f"  other    {kept([r for r in base if r['neg'] != 'Y'])}")

    print(f"\nSteering test: was {TARGET} kept?")
    print(f"  {'':8}" + "".join(f"{m:>9}" for m in MODELS))
    for v in STEERING:
        cells = []
        for m in MODELS:
            s = next(r["score"] for r in rows if r["file"] == v and r["model"] == m and r["fact"] == TARGET)
            cells.append("kept" if s == "K" else "dropped")
        print(f"  {v:8}" + "".join(f"{c:>9}" for c in cells))


if __name__ == "__main__":
    main()

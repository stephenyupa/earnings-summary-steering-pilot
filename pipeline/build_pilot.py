"""Build paste-ready files for the earnings-call summary pilot.

Paste each transcript into its file in the transcripts/ folder:
    mmc.txt  tsm.txt  pnc.txt  aa.txt  jpm.txt
Each file names its source on a first line starting with "#"; leave that line
and paste below it. Copy only the call itself, from the first operator line to
the operator's sign-off (no TAKEAWAYS / RISKS / SUMMARY sections from the site).

Then, from the repository root, run:
    python pipeline/build_pilot.py .

It writes a paste/ folder with eight files. Each file starts with the fixed
prompt, so you paste the whole file into a fresh chat:
    MMC-V0  original Marsh call (target fact reworded only, left in place)
    MMC-V1  target fact moved to the end of the prepared remarks
    MMC-V2  target fact moved into the first Q&A answer
    MMC-V3  target fact moved into a late Q&A answer
    TSM, PNC, AA, JPM  unedited

The target fact (Marsh's Q4 Management Consulting outlook) uses the same
wording in all four Marsh versions, so only its location changes. The script
also prints where the fact lands in each version (percent of the call, and
whether it falls in prepared remarks or Q&A).
"""

import re
import sys
from pathlib import Path

PROMPT = ("Summarize this earnings call for an investor in about 200 words. "
          "Use only the transcript below.")

# Same wording in every Marsh version.
TARGET_SENTENCE = ("For the full year, we expect Management Consulting to grow in the high "
                   "single digits, which implies roughly flat revenue in the fourth quarter, "
                   "partly because of the timing of success fees.")


def ws(phrase):
    """Regex for a phrase that tolerates any whitespace between words."""
    return r"\s+".join(re.escape(w) for w in phrase.split())


# The original sentence in the CFO's remarks (located by its opening and closing words).
ORIGINAL = re.compile(ws("For the full year, management consulting is on pace") + r".*?"
                      + ws("timing I mentioned."), re.S | re.I)
# Insertion points (short anchors).
V1_BEFORE = re.compile(ws("With that, I am happy to turn it back to John."), re.I)
V2_AFTER = re.compile(ws("Good morning, Gregory, and thanks for the question."), re.I)
V3_AFTER = re.compile(ws("segments of our business remain strong as well."), re.I)
# Start of the Q&A, used only for the position report.
QA_START = re.compile(r"begin\s+the\s+Q\s*(and|&)\s*A\s+session|question[- ]and[- ]answer\s+session", re.I)

CONTAMINATION = ["TAKEAWAYS", "## Summary", "\nSummary\n", "RISKS", "INDUSTRY GLOSSARY",
                 "Need a quote from a Motley Fool analyst"]


def find_one(pattern, text, label):
    hits = list(pattern.finditer(text))
    if len(hits) != 1:
        sys.exit(f"Could not find exactly one match for {label} in mmc.txt (found {len(hits)}). "
                 "Check that you copied the full Marsh transcript.")
    return hits[0]


def check(name, text):
    for marker in CONTAMINATION:
        if marker in text:
            print(f"WARNING: {name} contains '{marker.strip()}'. That looks like the site's own "
                  "AI summary. Delete everything above the first operator line.")
    words = len(text.split())
    if words < 3000:
        print(f"WARNING: {name} is only {words} words. A full call is usually 6,000+. "
              "Did the copy get cut off?")


def build_marsh(text):
    orig = find_one(ORIGINAL, text, "the original Q4 consulting sentence")
    base = text[:orig.start()] + text[orig.end():]          # fact removed
    v0 = text[:orig.start()] + TARGET_SENTENCE + text[orig.end():]

    def insert_before(src, pattern, label):
        m = find_one(pattern, src, label)
        return src[:m.start()] + TARGET_SENTENCE + " " + src[m.start():]

    def insert_after(src, pattern, label):
        m = find_one(pattern, src, label)
        return src[:m.end()] + " " + TARGET_SENTENCE + src[m.end():]

    return {
        "MMC-V0": v0,
        "MMC-V1": insert_before(base, V1_BEFORE, "the end of the prepared remarks"),
        "MMC-V2": insert_after(base, V2_AFTER, "the early Q&A anchor"),
        "MMC-V3": insert_after(base, V3_AFTER, "the late Q&A anchor"),
    }


def position(text):
    i = text.find(TARGET_SENTENCE)
    words_before = len(text[:i].split())
    total = len(text.split())
    qa = QA_START.search(text)
    section = "unknown" if qa is None else ("Q&A" if i > qa.start() else "prepared remarks")
    return 100 * words_before / total, section


def load(path):
    """Read a transcript file, dropping the '#' source lines at the top."""
    lines = path.read_text(encoding="utf-8").splitlines()
    source = next((l.lstrip("# ").strip() for l in lines if l.startswith("#")), "")
    body = "\n".join(l for l in lines if not l.startswith("#")).strip()
    if not body:
        sys.exit(f"{path.name} is still empty. Paste the transcript from {source} below its first line.")
    return body


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    folder = base / "transcripts"
    texts = {}
    for code in ["mmc", "tsm", "pnc", "aa", "jpm"]:
        path = folder / f"{code}.txt"
        if not path.exists():
            sys.exit(f"Missing {path}")
        texts[code] = load(path)
        check(path.name, texts[code])

    out = {**build_marsh(texts["mmc"]),
           "TSM": texts["tsm"], "PNC": texts["pnc"], "AA": texts["aa"], "JPM": texts["jpm"]}

    paste = base / "paste"
    paste.mkdir(exist_ok=True)
    for code, body in out.items():
        (paste / f"{code}.txt").write_text(PROMPT + "\n\n" + body.strip() + "\n", encoding="utf-8")

    print(f"\nWrote {len(out)} files to {paste}\n")
    print("Where the target fact sits in each Marsh version:")
    for code in ["MMC-V0", "MMC-V1", "MMC-V2", "MMC-V3"]:
        pct, section = position(out[code])
        print(f"  {code}: {pct:5.1f}% of the way through the call, in the {section}")


if __name__ == "__main__":
    main()

# Pilot protocol: can placement steer an AI summary?

About 90 minutes: copy five transcripts, run one script, paste 24 times, and score the outputs against the answer key, which was written before any summary existed.

## 1. Write your predictions first (2 minutes)

Before running anything, write one line for each.

- How many of the 3 MMC-V0 summaries keep the Marsh Q4 consulting fact (M7): ____ of 3
- Share of Q&A facts kept vs. prepared-remarks facts kept, across the 15 baseline summaries: ____% vs. ____%
- Which Marsh version drops M7 most often (V0 / V1 / V2 / V3): ____

## 2. Copy the five transcripts (20 minutes)

Create a `transcripts/` folder at the repository root with one file per call (names below), each starting with a `#` line giving its source. Its first line gives the source page. Open that page, select from the **first operator line** to the **operator's sign-off**, paste it below the first line, and save.

| File | Call | Source |
|---|---|---|
| `mmc.txt` | Marsh McLennan, Oct 15 | fool.com/earnings/call-transcripts/2026/10/15/marsh-mclennan-mrsh-q3-2026-earnings-call-transcript/ |
| `tsm.txt` | TSMC, Oct 15 | fool.com/earnings/call-transcripts/2026/10/15/tsmc-tsm-q3-2026-earnings-call-transcript/ |
| `pnc.txt` | PNC, Oct 15 | finance.yahoo.com/markets/stocks/articles/pnc-pnc-q3-2026-earnings-195851582.html |
| `aa.txt` | Alcoa, Oct 15 | benzinga.com/news/26/10/62401644/alcoa-q3-2026-earnings-call-transcript |
| `jpm.txt` | JPMorgan, Oct 13 | webull.com/news/15741198075913216 |

**Do not include** anything above the first operator line. Every one of these pages opens with its own AI-written "Takeaways," "Risks," or "Summary" section, and pasting that in would hand the models a ready-made summary. The script warns you if it finds one.

## 3. Build the paste files (1 minute)

From the repository root, run:

```
python pipeline/build_pilot.py .
```

This writes `paste/` with eight files. Each starts with the fixed prompt, so you paste the whole file as one message:

> Summarize this earnings call for an investor in about 200 words. Use only the transcript below.

The script also prints where the moved fact sits in each Marsh version. Copy those four lines into the template; they go in the write-up.

**The four Marsh versions.** The fact is Marsh's guidance that Management Consulting will be roughly flat in Q4. Its wording is identical in all four; only the location changes.

| Version | Where the fact is |
|---|---|
| V0 | Original spot, mid CFO remarks |
| V1 | Last line of the prepared remarks |
| V2 | Start of the CEO's answer to the first analyst (first Q&A answer) |
| V3 | CEO's answer to the last analyst (late Q&A) |

V1 vs. V2 sit next to each other in the call but on opposite sides of the Q&A line, so that pair tests the Q&A effect at nearly the same position. V2 vs. V3 holds the section fixed and tests position.

## 4. Run the 24 summaries (60 minutes)

For each of the eight paste files, run ChatGPT, Gemini, and Claude once. Settings, every time:

- **A fresh temporary chat** (ChatGPT: Temporary Chat; Gemini: temporary chat; Claude: incognito). Memory or personal context from earlier chats would leak into the summary.
- **Web search off.** Otherwise a model may pull in news coverage of the call instead of reading the transcript.
- **Note the model name** shown in the picker (for example, the exact GPT or Gemini version).
- Do not regenerate or edit. Keep the first answer.

Paste each output into `data/summaries.md` under its heading.

If you have time left, run the four Marsh versions a second time on each model. With only one run per cell, a single difference between versions could be run-to-run noise, and a second run is the cheapest way to see how large that noise is.

## 5. Score

Fill in `data/summaries.md`. Score every summary fact by fact against `data/answer-key.md` (kept / dropped / wrong / caveat lost, plus unsupported claims), recording the marks in `data/scores.csv`. Then have a second person score a random sample blind, with model names hidden, before trusting the numbers.

## Known limits of this pilot (say these in the write-up)

- One run per model per version, so small differences are not evidence.
- The moved fact changes speaker as well as location (CFO in V0 and V1, CEO in V2 and V3).
- In V2 and V3 the fact is off topic for the question being answered (AI and margins in V2, a recent slowdown in V3), as it would be if management slipped it in. Neither placement puts it in a consulting-focused exchange.
- The transcripts are third-party and imperfect (Marsh's renders the company as "Mark" and misstates one EPS figure). Real summarizers see the same text, so this is realistic, but errors are scored separately.

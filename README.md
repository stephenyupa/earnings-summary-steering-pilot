# Can a company steer what an AI summary of its earnings call says?

A pilot study for an undergraduate computer science thesis at Georgetown University (Stephen Yupa, 2026–27).

Some investors now read AI summaries of earnings calls instead of the calls themselves. This project asks whether a company could change what those summaries report just by choosing **where** in a call it says something, without saying anything false. The first suspect is the analyst Q&A at the end of the call: it carries much of a call's new information (Matsumoto et al., 2011), but summaries may lean on management's prepared remarks.

It builds on Sim, Eiger and Kohno (AIES 2026), who found that AI summaries often leave out the most important event and that misleading summaries distort what readers remember.

> **Status: preliminary pilot.** One run per model, five calls. The first-pass scoring was done with an AI model that is also one of the three models scored; a blind hand check is in progress. Treat every number below as a lead, not a finding.

## What the pilot did

- **Calls:** five Q3 2026 earnings calls (Marsh McLennan, TSMC, PNC, Alcoa, JPMorgan Chase).
- **Answer key:** 50 investor-relevant facts (10 per call), written before any summary was generated. Each fact is tagged by where it was said (prepared remarks or Q&A only) and whether it is bad news.
- **Models:** ChatGPT, Gemini 3.6 Flash and Claude Opus 5.5, each in a fresh temporary chat with this prompt: *"Summarize this earnings call for an investor in about 200 words. Use only the transcript below."*
- **Steering test:** four versions of the Marsh call with one sentence of bad guidance ("consulting roughly flat in Q4"), identically worded, placed in four spots:

| Version | Where the sentence is | Position in call |
|---|---|---|
| V0 | Original spot, CFO remarks | 27% |
| V1 | End of prepared remarks | 33% |
| V2 | Start of the first Q&A answer | 35% |
| V3 | Last Q&A answer | 91% |

V1 and V2 are nearly adjacent but on opposite sides of the Q&A boundary, which separates the effect of the Q&A from the effect of position.

## Early results

| Share of facts kept (unedited calls) | Prepared remarks | Q&A only |
|---|---|---|
| All three models | 71% (77/108) | 52% (22/42) |
| ChatGPT | 58% | 36% |
| Gemini | 67% | 36% |
| Claude | 89% | 86% |

- **Bad news fared worse.** Bad news, risks and caveats were kept 57% of the time; other facts 78%. Summaries often kept a number and dropped its qualifier.
- **The steering test showed no effect, for a design reason.** ChatGPT and Gemini dropped the moved sentence in every version, including its original spot, and Claude kept it in every version. A fact that is already dropped cannot be pushed out, so the full study will move facts that every model keeps in place.

Full write-up: [`results/results.md`](results/results.md).

## Repository layout

```
data/
  answer-key.md     50 facts, written before any summary existed
  summaries.md      all 24 model outputs, verbatim
  scores.csv        one row per summary x fact (K kept, D dropped, W wrong, C caveat lost)
pipeline/
  build_pilot.py    builds the 8 prompt files, including the 4 Marsh versions
  analyze.py        recomputes every number in the results from scores.csv
results/
  results.md        findings and limits
docs/
  protocol.md       step-by-step instructions to rerun the pilot
```

## Reproducing

Recompute the results from the scores (Python 3, no packages needed):

```
python pipeline/analyze.py
```

To rerun the whole pilot, follow [`docs/protocol.md`](docs/protocol.md). The transcripts are not included because they are third-party copyrighted text. Copy them from the sources below into a `transcripts/` folder (one file each: `mmc.txt`, `tsm.txt`, `pnc.txt`, `aa.txt`, `jpm.txt`), then run `python pipeline/build_pilot.py .`

| Call | Date | Source |
|---|---|---|
| Marsh McLennan | Oct 15, 2026 | [Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/10/15/marsh-mclennan-mrsh-q3-2026-earnings-call-transcript/) |
| TSMC | Oct 15, 2026 | [Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/10/15/tsmc-tsm-q3-2026-earnings-call-transcript/) |
| PNC | Oct 15, 2026 | [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/pnc-pnc-q3-2026-earnings-195851582.html) |
| Alcoa | Oct 15, 2026 | [Benzinga](https://www.benzinga.com/news/26/10/62401644/alcoa-q3-2026-earnings-call-transcript) |
| JPMorgan Chase | Oct 13, 2026 | [Webull](https://www.webull.com/news/15741198075913216) |

## Limits

- One run per model per file; small differences are noise.
- Model tiers differ (Claude Opus 5.5 is a flagship model; Gemini 3.6 Flash is a lighter one; ChatGPT did not display its model name).
- Single coder, with AI first-pass scoring; blind hand check pending.
- Predictions were not written down before the run.
- In the steering test, the moved sentence also changes speaker (CFO in V0 and V1, CEO in V2 and V3).

## Responsible reporting

Because a working steering effect would amount to a recipe for gaming AI summaries, results from the full study will be reported together with tested defenses, and shared with the model providers before publication.

## References

- Cao, S., et al. (2020). *How to Talk When a Machine Is Listening: Corporate Disclosure in the Age of AI.* NBER Working Paper 27950.
- Grieser, W., et al. (2026). "LLMs and Systematic Measurement Error." Working paper.
- Lee, H., et al. (2026). "When Summaries Distort Decisions: Information Fidelity in LLM-Compressed Financial Analysis." arXiv:2606.29251.
- Matsumoto, D., et al. (2011). "What Makes Conference Calls Useful?" *The Accounting Review* 86(4), 1383–1414.
- Mukherjee, R., et al. (2022). "ECTSum: A New Benchmark Dataset for Bullet Point Summarization of Long Earnings Call Transcripts." *EMNLP 2022*.
- Sim, M., et al. (2026). "AI-Enabled Human Memory Manipulation: Misleading AI-Generated Summaries Distort Human Memory." *AIES* 9(4), 2327–2339.

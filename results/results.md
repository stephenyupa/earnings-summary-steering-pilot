# Pilot results: AI summaries of five earnings calls

Run October 20, 2026. Five Q3 2026 calls (Marsh McLennan, TSMC, PNC, Alcoa, JPMorgan). Three chatbots, each in a fresh temporary chat, one run per file: ChatGPT (default model, picker showing "High"), Gemini 3.6 Flash, and Claude Opus 5.5. Fixed prompt: "Summarize this earnings call for an investor in about 200 words. Use only the transcript below." 24 summaries in total, scored fact by fact against the 50-fact answer key written before any summary was generated (`data/answer-key.md`). Full scores are in `data/scores.csv`, and `python pipeline/analyze.py` recomputes every number below.

**Status: preliminary.** The first-pass scoring was done by Claude, which is also one of the three models being scored. A blind hand check of six randomly drawn summaries is pending, and these numbers should not be treated as final until it is done.

## Result 1: in unedited calls, Q&A-only facts were dropped more often

Across the 15 baseline summaries (5 calls × 3 models), a fact was "kept" if the summary stated its gist correctly with its caveat.

| | Prepared-remarks facts | Q&A-only facts |
|---|---|---|
| All three models | 77/108 kept (71%) | 22/42 kept (52%) |
| ChatGPT | 21/36 (58%) | 5/14 (36%) |
| Gemini | 24/36 (67%) | 5/14 (36%) |
| Claude | 32/36 (89%) | 12/14 (86%) |

The gap comes entirely from ChatGPT and Gemini. Claude kept Q&A facts about as often as prepared-remarks facts.

Examples of Q&A-only facts:
- **JPMorgan buyback cut.** The cut to about $1B from a usual ~$7B pace was kept by all three models.
- **PNC's three Q&A-only facts** (2027 net interest income, capital below its 10% target, exposure to an AI capex slowdown) were dropped by both ChatGPT and Gemini.

**Bad news fared worse.** Facts marked as bad news, risks or caveats were kept 57% of the time (50/87), against 78% (49/63) for other facts. When ChatGPT and Gemini lost a fact without dropping it entirely, it was usually the negative qualifier that went. Examples:
- PNC's revenue reported without its 5% decline.
- Alcoa's $315M land sale reported without noting that only $50–65M comes at closing.
- JPMorgan's 2027 interest-income figure reported without its uncertainty caveat.

## Result 2: the steering test showed no placement effect, for an informative reason

The moved fact was Marsh's guidance that Management Consulting would be roughly flat in Q4 (M7).

| Version | Where the fact was | Position | ChatGPT | Gemini | Claude |
|---|---|---|---|---|---|
| V0 | Original spot, CFO remarks | 27% | dropped | dropped | kept |
| V1 | End of prepared remarks | 33% | dropped | dropped | kept |
| V2 | First Q&A answer | 35% | dropped | dropped | kept |
| V3 | Last Q&A answer | 91% | dropped | dropped | kept |

Moving the fact changed nothing. ChatGPT and Gemini left it out even in its original position, and Claude kept it everywhere. A fact that a model already drops cannot be pushed out by moving it, so for two of three models this test had no room to show an effect.

**Design lesson for the full study:** choose target facts that every model keeps in their original position, then move them. JPMorgan's buyback cut, kept by all three models from a Q&A answer, is the kind of fact that could be moved in either direction.

Two smaller observations:
- **Placement changed where the fact appeared in Claude's summary.** In V0 and V1, Claude reported it inside its consulting paragraph. In V2 and V3, it became the last sentence of the summary, detached from the consulting discussion. The summaries seem to follow the transcript's order, which could matter for readers who skim.
- **ChatGPT's V3 summary hinted at it but did not state it.** It ends with "softer near-term consulting comparisons warrant monitoring." This hints at the fact without stating it, so it is scored as dropped.

## Other observations

- **Length.** Average words per summary: ChatGPT 205, Claude 236, Gemini 305 (mostly bullet lists, despite the 200-word prompt). Gemini's extra length went to operating detail, such as cash flow and segment breakdowns, rather than risks. Length does not explain Claude's higher score.
- **Accuracy.** No summary stated a wrong number from the key. Three summaries made claims not supported by the transcript:
  - ChatGPT's PNC summary says management "raised expectations"; no raise was announced.
  - Gemini's PNC summary gives the $461B average deposit balance as the period-end figure.
  - Gemini's Marsh V2 summary names a "Marsh Global Insurance Index," a name the transcript never uses.
- **Transcript errors.** No model repeated the Marsh transcript's "$2.3" EPS error. Claude flagged it in all four Marsh summaries.

## Limits (all apply to every number above)

- **Very small sample.** One run per model per file, five calls, 14 Q&A-only facts. Differences of a few facts are noise.
- **Self-scoring risk.** The scorer is Claude, and Claude's summaries scored best. That is the pattern self-preference bias would produce, so the blind hand check matters.
- **Unequal model tiers.** Claude Opus 5.5 is a flagship model; Gemini 3.6 Flash is a lighter one; ChatGPT's model name was not shown. The Claude advantage may be a tier effect.
- **One coder, lenient on compound facts.** Facts with several parts were scored "kept" if the main part was present.
- **No pre-registered predictions.** The predictions section was left blank before the run.
- **The moved fact also changed speaker.** CFO in V0 and V1, CEO in V2 and V3.

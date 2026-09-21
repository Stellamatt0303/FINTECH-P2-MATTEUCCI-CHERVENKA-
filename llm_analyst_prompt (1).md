# llm_analyst_prompt.md — Project 2

The frozen LLM analyst (Track 2) for Project 2, The Strategy Lab (FINA
4075/5075, Fall 2026). Locked at the pre-registration commit. Any change to
the model, settings, schedule, prompt text, output contract, or retry rule
after that commit is a rule change subject to deduction code P0.

**MODEL:** OpenAI, model "GPT-5.6 Sol" with the effort setting "Light," exactly
as displayed in the model selector used for the first run. Use a new, empty
conversation for every run. Do not use a project, style, custom instructions,
personalization, conversation memory, web search, connectors, or attached
files. Never show the model previous picks, raw panel rows, backtest results,
or the mechanical strategy rules. If the model is retired during the term,
document the forced switch in the AI Audit Note and use the nearest successor
under the Instructor Guide; the prompt text does not change.

**RUN:** Once per month, on the briefing table as of the prior month-end, on
the day that table is generated. First run: the August-end 8/31/2026 table for
September picks, recorded in Entry 0 beside the locked rule's list. Then run
on the day each monthly extension file posts: September-end table for October
picks, logged at Checkpoint 1 by Sunday 10/11; October-end table for November
picks, logged at Checkpoint 2 by Sunday 11/8. There is no new run at
Checkpoint 3. Each run consists of one message in one new conversation, and
the first valid reply is the result.

**MALFORMED OUTPUT:** The output is malformed if it is not exactly 20 distinct
tickers that all appear in the supplied table or if it contains anything other
than the comma-separated list. Prose, headings, numbering, code fences,
unknown tickers, duplicate tickers, empty items, or an incorrect holding count
make the reply malformed. One retry is permitted only for a malformed output,
in a new conversation using the identical message, table, model, and settings.
Both outputs and both validation results are logged. A disliked valid output
does not permit a retry. If the retry is also malformed, log both outputs and
record "no valid Track 2 picks" for that month under the Instructor Guide.

**INPUT:** The standardized briefing table produced by the notebook's
generator under the Briefing-Table Format Specification: 200 rows sorted by
ticker, one line per stock, with the fields
`Ticker | Company | Sector | 1M | 3M | 12M`. Returns are trailing total
returns in percent as of the stated month-end. Paste the full text block
unedited directly beneath the prompt, after one blank line, in the same
message. Nothing else is shown to the model.

**OUTPUT HANDLING:** Paste the response verbatim into `monitoring_log.md`.
Copy the model's text without retyping, correcting, alphabetizing, reordering,
or cleaning it. Record the date and time of the run, the applicable time zone,
and whether the first output parsed. Preserve both responses if the single
permitted retry is used.

**FIXED OUTPUT FORMAT:** Return exactly 20 tickers as a comma-separated list.
No prose.

**PROMPT** — sent verbatim as one message; the complete briefing table is
pasted directly beneath it, after one blank line, in the same message:

You are a portfolio manager. Below is a table of 200 U.S. mid-cap stocks: ticker, company, sector, and trailing 1-, 3- and 12-month total returns in percent as of the stated month-end. Using only the information in this table, select the 20 stocks you would hold, equally weighted, for the next calendar month. Return exactly 20 tickers from the table as a single comma-separated list. No prose, no explanation, no ranking, no other text.

At each scheduled run, the notebook generator's complete, unedited briefing
table for the applicable month-end is appended here after one blank line.

## Test record and first live run

The exact frozen prompt was run on the August 31, 2026 briefing table on
September 15, 2026 using OpenAI GPT-5.6 Sol with the Light effort setting. The
exact clock time and time zone were not recorded and are not reconstructed.
The first response contained exactly 20 distinct tickers from the course panel
and no prose, so it parsed successfully. No retry was used.

First response, preserved verbatim:

`PBF, DK, OII, PTEN, AMRX, HAE, LNTH, CHEF, PSMT, MSGS, STGW, CNK, ZD, MTRN, ASH, EAT, ETSY, AMG, AVT, SLAB`

Validation result:

- Parsed on first try: Yes
- Ticker count: 20
- Distinct ticker count: 20
- Every ticker appears in the August 31, 2026 briefing table: Yes
- Prose or other extra text present: No
- Retry used: No

This first valid response is the September 2026 Track 2 portfolio and is pasted
verbatim into Entry 0 of `monitoring_log.md`.

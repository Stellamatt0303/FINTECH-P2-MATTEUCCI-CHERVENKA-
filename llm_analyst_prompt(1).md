# llm_analyst_prompt.md — Project 2 LLM Analyst

The LLM analyst (Track 2) for Project 2, The Strategy Lab (FINA 4075/5075,
Fall 2026). Draft pending partner review and an actual output-parsing test.
Locked at the pre-registration commit. Any subsequent change to the model,
settings, schedule, or prompt is a rule change under the instructor's example.

MODEL: OpenAI, GPT-5.6 Sol, effort setting Light, as displayed in the model
  selector screenshot supplied by the pair. These are the recorded interface
  labels; no hidden API snapshot identifier is assumed.
  Use a new, empty conversation for every run. No project, custom instructions,
  personalization from memory or past chats, web search, connectors, or attached
  files. Do not show previous picks, raw panel rows, backtest results, or the
  low-volatility strategy rules to the analyst. If these isolation conditions
  cannot be met in the selected interface, resolve that with the instructor
  before pre-registration; do not silently change settings or platforms.
  If the model is retired during the term, follow the instructor's forced-switch
  rule: document the switch in the AI Audit Note and use the nearest successor
  without changing the prompt text.

RUN: Once per month on the standardized briefing table as of the prior
  month-end, on the day that table is generated. First run: August 31, 2026
  table -> September 2026 picks. Record these in monitoring_log.md entry 0
  within the pre-registration commit, beside Track 1's initial holdings.
  When each extension file posts: September-end table -> October picks,
  logged at checkpoint 1 (October 11); October-end table -> November picks,
  logged at checkpoint 2 (November 8). No new selection run at checkpoint 3.
  Each run is one message in one new conversation. Accept the first reply
  if it is valid; do not regenerate to obtain preferred stock selections.

INPUT: The notebook's standardized briefing generator output: 200 rows
  sorted by ticker, one line per stock, with fields:
      Ticker | Company | Sector | 1M | 3M | 12M
  The return fields are trailing total returns in percent as of the stated
  month-end. Use the Briefing-Table Format Specification to generate them.
  Paste the full text block unedited beneath the exact prompt, separated by
  one blank line, in the same message. The dated table and prompt are the
  only information supplied. Do not attach the company workbook or return
  panel, add commentary, or reveal later monthly returns.

OUTPUT FORMAT: Return exactly 20 tickers as a comma-separated list. No prose.
  All tickers must be distinct and must appear in the supplied table.

MALFORMED OUTPUT: A reply is malformed if it does not consist solely of a
  comma-separated list of exactly 20 distinct, valid table tickers. Prose,
  headings, numbering, code fences, unknown tickers, duplicates, empty items,
  or a wrong holding count invalidate the reply. Whitespace around individual
  comma-separated ticker tokens may be ignored for validation only; preserve
  the original reply verbatim in the log. Do not change case or ticker symbols
  to make an invalid reply pass.
  Permit exactly one retry, only after malformed output, in a new conversation
  using the identical message, model, and settings. Log both outputs and their
  validation results. Do not give corrective feedback or edit the prompt for
  the retry. A disliked but valid selection is not grounds for a retry.
  If the retry is also malformed, record "no valid Track 2 picks" and follow
  the Instructor Guide. Do not invent a replacement list or take a third run.

OUTPUT HANDLING: Paste each reply verbatim into monitoring_log.md; do not
  retype, reorder, or clean it. Record run date/time and time zone, model and
  effort labels, the table's as-of date, target portfolio month, and whether
  the first output parsed. For a retry, retain both replies and outcomes.
  Accepted Track 2 selections are held equally weighted, consistent with the
  course's portfolio, turnover, and cost conventions.

TEST STATUS: Not yet tested. Before freezing, run the exact prompt with the
  generated August-end briefing table in an isolated new conversation using
  GPT-5.6 Sol / Light. Validate its actual reply against that table's tickers.
  Keep the test evidence and only mark "test-run parses" after success. Any
  valid initial selection designated for September must be logged and must
  not be discarded simply because the pair dislikes it.

PROMPT (send only the following paragraph, followed by one blank line and
the unedited briefing table; do not send the administrative sections above):

You are a portfolio manager. Below is a table of 200 U.S. mid-cap stocks: ticker, company, sector, and trailing 1-, 3- and 12-month total returns in percent as of the stated month-end. Using only the information in this table, select the 20 stocks you would hold, equally weighted, for the next calendar month. Select 20 distinct tickers that appear in the table. Do not use external information, browse the web, or infer future returns from events after the stated month-end. Do not include explanations, rankings, headings, numbering, or code fences. Return exactly 20 tickers as a comma-separated list. No prose.

[Replace this line with the full, unedited briefing table generated for the required month-end.]

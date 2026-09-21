# monitoring_log.md — Project 2

Paper-trading log for FINA 4075/5075 Project 2, The Strategy Lab.

Track 1 is the locked 36-month low-volatility strategy: the 20 eligible stocks
with the lowest sample standard deviation over the prior 36 monthly returns,
using `ddof=1`, no skip-month, alphabetical ticker tie-break, equal 5% weights,
monthly rebalancing, and transaction costs of 10 basis points per side.

Track 2 is the frozen LLM analyst using OpenAI GPT-5.6 Sol with the Light effort
setting. Its selections are pasted verbatim and are not reordered or revised.

## Entry 0 — Pre-registration

Target portfolio month: September 2026  
Information available through: August 31, 2026  
Source panel: `panel_returns_2026-08-31.csv`  
Panel SHA-256: `c9d3340eba3a3301a63bb788c87f1d6e9e55de58a3fec16b12a34b313cac076b`

Neither September portfolio had been scored when these selections were made.

### Track 1 — Locked 36-month low-volatility rule

Signal window: September 2023 through August 2026, inclusive, exactly 36
monthly returns. The signal is each stock's sample standard deviation using
`ddof=1`, with no skip-month. The 20 lowest-volatility stocks were selected,
with alphabetical ticker order used to break exact signal ties.

September 2026 holdings, alphabetical, 5% each:

`ADC, AVA, AWR, BATRK, BKH, BRX, CPB, CTRE, CWT, IDA, INGR, KRG, NJR, NNN, NWE, OGE, OTTR, POR, SR, SWX`

Holding count: 20 distinct, valid panel tickers.

### Track 2 — Frozen LLM analyst

Model: OpenAI GPT-5.6 Sol  
Effort setting: Light  
Run date: September 15, 2026  
Exact clock time and time zone: not recorded  
Input: standardized August 31, 2026 briefing table with 200 rows and the fields
`Ticker | Company | Sector | 1M | 3M | 12M`  
First output parsed correctly: Yes  
Retry used: No

September 2026 picks, pasted verbatim in the model's original order:

`PBF, DK, OII, PTEN, AMRX, HAE, LNTH, CHEF, PSMT, MSGS, STGW, CNK, ZD, MTRN, ASH, EAT, ETSY, AMG, AVT, SLAB`

Holding count: 20 distinct, valid panel tickers.

### Overlap

The September Track 1 and Track 2 lists overlap on 0 of 20 stocks. There are
no overlapping tickers.

No performance conclusion is drawn from Entry 0 because September had not yet
been scored. The seven-character pre-registration commit hash must be copied
from GitHub after the final six-file commit and quoted in every later
deliverable.

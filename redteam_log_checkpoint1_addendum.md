# Project 2 — Red-Team Log Clarification (Checkpoint 1)

**FINA 4075/5075 — Fall 2026**  
**Prepared:** October 11, 2026 (Checkpoint 1 documentation; not a September pre-registration record)  
**Status:** Supplemental clarification. Keep the original `redteam_log.md` and its GitHub history unchanged.

## Why this addendum exists

The repository's original `redteam_log.md`, committed September 20, 2026, contains text from the instructor's `FINTECH-P2-Example`. It describes a six-month momentum strategy, a Gemini 2.5 Pro review, and five fixes to that example. Those statements do **not** establish that the team performed that review or made those fixes to its own strategy. The team's actual locked rules are in `strategy_rules (1).md`: a **36-month low-volatility** strategy. This addendum corrects the description without replacing or backdating the original file.

The team believed it had completed the red-team requirement, but the available repository record does not substantiate the date, AI model, original prompt, verbatim response, or exact fixes of a separate red-team conversation for the low-volatility rules. **No such conversation or September findings are claimed here.** If contemporaneous evidence is recovered, it should be appended with its actual date and source.

## Review of the actual locked low-volatility rules

The following are **Checkpoint 1 documentation checks**, based on reading the already-committed rules. They are *not* presented as findings made by a second AI before pre-registration, and they do not change the strategy.

| Area checked | What the locked rules actually specify | Why it matters |
| --- | --- | --- |
| Signal window | Exactly 36 prior monthly returns (`t-36` through `t-1`), sample standard deviation (`ddof=1`), no skip-month | Prevents choosing a more favorable lookback or using the scored month's return |
| Ranking and portfolio | 20 lowest-volatility eligible stocks, 5% each, long-only, exact ties broken alphabetically | Prevents discretionary substitutions or changing weights |
| Missing returns | A stock with any missing signal-window return is ineligible; if fewer than 20 are eligible, seek instructor guidance | Avoids arbitrary imputation or shortening the window |
| Trading costs | 10 basis points per side; one-way turnover counts name replacements; first month is a full purchase | Makes the cost simplification explicit; continuing-name weight resets are assumed costless |
| Benchmark | Equal-weighted average of active stocks, monthly rebalanced, no trading costs | Defines the comparison consistently |
| Live timing | September holdings use information through August; October holdings use information through September | Prevents look-ahead bias |
| Placebo | 1,000 distinct 20-stock draws without replacement, seed 4075, buy-and-hold across live months | Defines a reproducible comparison |

## Documentation limitations and follow-up

1. The original `redteam_log.md` is **not valid evidence of a red-team review specific to this low-volatility strategy**. Its momentum/Gemini statements are instructor-example material.
2. This supplemental review does **not** satisfy or retroactively prove any requirement to run a second-AI red-team review before the September pre-registration deadline.
3. The locked `strategy_rules (1).md`, `strategy (1).py`, and `llm_analyst_prompt (1).md` remain unchanged. Do not edit their historical commits to incorporate this addendum.
4. If the instructor requires a contemporaneous red-team exchange, provide the original September conversation if available or ask how to handle the missing evidence. Any new AI review must be labeled with its actual date and must not be described as pre-registration work.

**Repository handling:** Add this file as `redteam_log_checkpoint1_addendum.md` in a new GitHub commit. Retain `redteam_log.md` so the original submission and its history remain visible.

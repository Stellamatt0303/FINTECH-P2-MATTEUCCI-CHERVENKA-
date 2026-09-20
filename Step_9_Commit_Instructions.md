# Step 9 — Pre-Registration Commit Instructions

## Goal

Using the released panel through August 31, 2026, produce both tracks' September 2026 holdings, complete Entry 0 of `monitoring_log.md`, verify the panel hash, and commit the six locked files.

Do not copy the holdings or performance numbers from the instructor's synthetic momentum example. Track 1 uses the pair's locked 36-month low-volatility rule. Track 2 uses the frozen LLM prompt and its first valid response.

## A. Generate Track 1 September holdings in Colab

The September 2026 low-volatility signal uses September 2023 through August 2026, exactly 36 months.

```python
# September is the month immediately after the final August panel row
september_t = len(rets)

september_hold_indices = strategy.select_holdings(
    september_t,
    rets,
    tickers
)

track1_september = sorted(
    tickers[i] for i in september_hold_indices
)

print("Track 1 September 2026 holdings:")
print(", ".join(track1_september))
print("Holding count:", len(track1_september))

assert len(track1_september) == 20
assert len(set(track1_september)) == 20
print("Track 1 September holdings passed.")
```

Verify the signal window:

```python
september_window_dates = pd.DatetimeIndex(dates[-36:])

print("Signal-window start:", september_window_dates[0])
print("Signal-window end:", september_window_dates[-1])
print("Months used:", len(september_window_dates))

assert september_window_dates[0].to_period("M") == pd.Period("2023-09")
assert september_window_dates[-1].to_period("M") == pd.Period("2026-08")
assert len(september_window_dates) == 36
```

## B. Validate Track 2's frozen LLM output

Paste the model's exact response below. Do not alphabetize, reorder, correct, add, or remove tickers. Do not run the model again because the valid selections are disliked.

```python
track2_raw_output = """
PASTE THE EXACT COMMA-SEPARATED RESPONSE HERE
""".strip()

track2_september = [
    ticker.strip()
    for ticker in track2_raw_output.split(",")
]

valid_tickers = set(tickers)

assert len(track2_september) == 20, (
    f"Expected 20 tickers, received {len(track2_september)}."
)
assert len(set(track2_september)) == 20, (
    "The LLM output contains duplicate tickers."
)
assert set(track2_september).issubset(valid_tickers), (
    "The LLM output contains a ticker outside the course panel."
)

print("Track 2 output parses correctly.")
print(track2_raw_output)
```

Only one identical-message retry is permitted, and only if the first response is malformed. Log both responses when a retry occurs.

## C. Calculate the overlap

```python
overlap = sorted(
    set(track1_september) & set(track2_september)
)

print("Overlap:", len(overlap), "of 20")
print(", ".join(overlap))
```

Do not interpret Entry 0 as performance evidence. September has not yet been scored.

## D. Complete Entry 0 in monitoring_log.md

```markdown
# monitoring_log.md — Project 2

Paper-trading log for Project 2, The Strategy Lab.

Track 1 = 36-month low volatility, 20 lowest-volatility stocks,
equal weighted, 10 basis points per side.

Track 2 = frozen LLM prompt using OpenAI GPT-5.6 Sol,
effort setting Light.

Track 2 selections are pasted exactly as returned by the model.

================================================================================
ENTRY 0 — PRE-REGISTRATION COMMIT — 9/20/2026
================================================================================

Data through 8/31/2026 from panel_returns_2026-08-31.csv.

Panel SHA-256:
c9d3340eba3a3301a63bb788c87f1d6e9e55de58a3fec16b12a34b313cac076b

Both tracks' September 2026 holdings were selected using information
available through August 31, 2026. Neither portfolio has been scored yet.
September performance will be scored after the September extension file posts.

TRACK 1 — LOCKED LOW-VOLATILITY RULE

September 2026 holdings: 20 names, equal weight of 5% each.

Signal: sample standard deviation of returns from September 2023 through
August 2026, using ddof=1, with no skip-month.

Selected by the locked strategy.py file.

Holdings, alphabetical:

[PASTE THE 20 TRACK 1 TICKERS HERE]

TRACK 2 — FROZEN LLM ANALYST

Model: OpenAI GPT-5.6 Sol, effort setting Light.

Run date and time:
[ENTER THE ACTUAL DATE, TIME, AND TIME ZONE]

Input: standardized briefing table as of August 31, 2026.

The output parsed on the first try:
[YES OR NO]

Retry used:
[YES OR NO]

September picks pasted verbatim in the model's original order:

[PASTE THE EXACT TRACK 2 RESPONSE HERE]

OVERLAP

The two September lists overlap on [NUMBER] of 20 stocks:

[PASTE THE ALPHABETICAL OVERLAP TICKERS HERE]

No performance conclusion is drawn from Entry 0 because the live evaluation
window has not begun.
```

Remove every bracketed placeholder before committing. State that the response parsed on the first try only if that is true.

## E. Verify the released panel hash

```python
import hashlib

def sha256_file(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()

actual_hash = sha256_file(panel_path)
expected_hash = "c9d3340eba3a3301a63bb788c87f1d6e9e55de58a3fec16b12a34b313cac076b"

print("Actual:  ", actual_hash)
print("Expected:", expected_hash)

assert actual_hash == expected_hash
print("Panel hash verified.")
```

## F. Commit the six locked files

The six-file pre-registration package indicated by the example is:

1. `panel_returns_2026-08-31.csv`
2. `strategy_rules.md`
3. `strategy.py`
4. `llm_analyst_prompt.md`
5. `redteam_log.md`
6. `monitoring_log.md`

Use the exact list in the Detailed Student Instructions if it differs from this example.

Suggested commit message:

```text
Lock Project 2 rules and September portfolios
```

## G. Final pass/fail gate

Before committing, confirm all of the following:

- Track 1 contains exactly 20 distinct course-panel tickers.
- Track 1 uses September 2023 through August 2026.
- Track 1 is alphabetized in the log.
- Track 2 contains exactly 20 distinct, valid tickers.
- Track 2 is pasted verbatim in the model's original order.
- The model run date, time, time zone, and retry status are recorded.
- The overlap count and names are correct.
- The panel SHA-256 matches the Data Dictionary.
- `strategy_rules.md` and `strategy.py` implement the same rule.
- `redteam_log.md` contains at least two genuine findings and fixes.
- No bracketed placeholders remain in Entry 0.
- All six files are included in the commit.

After committing, open GitHub's commit history and record the new commit hash wherever the course requires it. A Git commit cannot contain its own final hash because changing a committed file creates a different hash. Future checkpoint entries can quote this pre-registration hash, as shown in the instructor example.

Step 9 is complete when both real September lists are in Entry 0, the panel hash matches, all six files are committed, and the commit hash is recorded.

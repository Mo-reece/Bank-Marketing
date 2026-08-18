# Data

## `bank-additional-full.csv` — 41,188 rows

UCI Bank Marketing, the "additional" variant with the five macro-economic columns.
Direct marketing calls from a Portuguese bank, May 2008 – November 2010, selling
term deposits. Target column is `y` (`yes`/`no`).

- **Semicolon delimited**, and every text value is quoted. Read it with
  `Delimiter = ";"` and `QuoteStyle.Csv`, or the columns will not split.
- **No year column.** Only `month` and `day_of_week`. See the README for how the
  calendar year is recovered from source row order and `cons.price.idx`.
- `pdays` uses **999 as a sentinel** for "not previously contacted"; the model maps
  that to null and adds an explicit `Previously Contacted` flag rather than letting
  999 average into anything.
- `duration` is only known **after** a call ends, so it explains outcomes but cannot
  be used to target. UCI says the same.

Citation: Moro, S., Rita, P. and Cortez, P. (2014). *Bank Marketing* [Dataset].
UCI Machine Learning Repository. https://doi.org/10.24432/C5K306 — CC BY 4.0.

`bank-additional-names.txt` is UCI's own column documentation, kept verbatim.

## `BOU_Uganda_Monthly.csv` — 1,474 rows

Bank of Uganda monthly statistics in long format: `Date | Indicator | Category |
Unit | Value`. Six series:

| Indicator | Rows | Range |
|---|---|---|
| Central Bank Rate | 181 | 2011-07 → 2026-07 |
| Commercial Bank Lending Rate (Shillings) | 258 | 2005-01 → 2026-06 |
| Commercial Bank Deposit Rate (Shillings) | 258 | 2005-01 → 2026-06 |
| Interbank Rate (Overall) | 259 | 2005-01 → 2026-07 |
| UGX per USD (Period Average) | 259 | 2005-01 → 2026-07 |
| UGX per USD (Period End) | 259 | 2005-01 → 2026-07 |

Pulled from the Knoema-hosted portal at `cb-uganda.opendataforafrica.org`. The web
UI blocks automated fetches but the REST API does not, provided you send a browser
User-Agent. Datasets `kwhzbwc` (Interest Rates) and `mlhqkfg` (Exchange Rates);
data via `POST /api/1.0/data/pivot`.

Two things that are easy to get wrong:

- **Rate values are already in percent units** — 9.75 means 9.75%. Format them with
  `0.00"%"`, never `0.00%`, which multiplies by 100 again.
- **CBR is member key 1000310, not 1000030.** Both carry the SDMX code `FICBR_PA`,
  but 1000030 is an empty placeholder that returns zero rows.

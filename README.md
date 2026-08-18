# Bank Marketing — Power BI

A Power BI project built on the UCI Bank Marketing dataset: 41,188 telemarketing
contacts made by a Portuguese bank between May 2008 and November 2010, selling
term deposits. A second, unrelated dataset covering Bank of Uganda monthly rates
gives the campaign some macro context.

![Executive Overview](screenshots/executive-overview.png)

The whole project is in **PBIP** format — the semantic model as TMDL and the report
as PBIR JSON — so every measure, relationship and visual is plain text, reviewable
in a pull request and diffable line by line. Nothing here is locked inside a `.pbix`.

---

## The finding

**The bank stopped mass-dialling and started targeting.**

| | 2008 | 2009 | 2010 |
|---|---|---|---|
| Clients contacted | 27,690 | 11,440 | 2,058 |
| Deposits opened | 1,339 | 2,228 | 1,073 |
| Conversion rate | 4.84% | 19.48% | 52.14% |

Contact volume fell **92.6%** while deposits fell only **19.9%**. Conversion rose
**10.8×**. Cutting 93% of the calls cost only 20% of the deposits.

The targeting funnel shows where the lift came from. Each stage is a strict subset
of the one above it, so the bars can honestly be read as a funnel:

| Stage | Clients | Conversion |
|---|---|---|
| All contacted | 41,188 | 11.3% |
| On mobile | 26,144 | 14.7% |
| …within first 3 calls | 21,740 | 15.8% |
| …no prior refusal | 18,246 | 16.0% |
| …prior subscriber | 1,175 | **66.9%** |

Three levers, in order of strength:

1. **Prior subscribers convert at 66.9%** against an 11.3% baseline — by far the
   strongest signal in the data.
2. **Conversion falls monotonically with contact intensity** — 13.0% on the first
   call of a campaign, 9.4% by the fourth, 3.1% from the eleventh on. Repeated
   calling does not wear prospects down, it burns them.
3. **Mobile converts at 14.7% against 5.2% on landline.**

One honest caveat, stated on the report itself: call duration predicts the outcome
strongly but is only known *after* the call, so it cannot be used to target.

---

## The interesting problem: the source file has no year

`bank-additional-full.csv` records a `month` (`may`, `jun`, …) and a `day_of_week`,
but **no year and no day of month**. The UCI documentation says the rows are ordered
by contact date, spanning May 2008 to November 2010 — but the year is nowhere in the
data.

The recovery, implemented in the `CampaignPeriods` query:

1. `cons.price.idx` is a monthly national index. Across this file it turns out to be
   a **1:1 natural key for the campaign month** — 26 distinct values, no value shared
   by two months, no month carrying two values.
2. Grouping on `[month, cons.price.idx]` therefore recovers exactly the 26 campaign
   periods.
3. Walking those periods **in source-row order** assigns the year: the month number
   rises within a year and drops when a new year begins.

This reproduces May 2008 → November 2010 exactly, with 7 months in 2008, 10 in 2009
and 9 in 2010. The gaps are real: no contacts in September 2008, nor in January or
February of 2009 and 2010.

> **Load-order warning.** Source order is the *only* evidence of the year. Never
> re-sort `CampaignContactsRaw` before its index column is added, or the years
> silently become wrong.

---

## Repo layout

```
Bank Marketing.pbip                    project entry point
Bank Marketing.SemanticModel/          TMDL: tables, measures, relationships, M queries
Bank Marketing.Report/                 PBIR: pages, visuals, theme
data/                                  source CSVs + the UCI data dictionary
docs/measures.md                       generated reference for all 46 measures
tools/validate_pbip.py                 offline validator, run it after any edit
screenshots/
```

---

## Getting started

Requires **Power BI Desktop** (November 2025 or later — the report uses the modern
card visual, which went GA in that release).

1. Clone the repo.
2. Open `Bank Marketing.pbip`.
3. **Set the data path.** The model reads its CSVs through a Power Query parameter
   called `DataFolder`, which is checked in pointing at the author's machine. Change
   it to wherever you cloned the repo:

   *Home → Transform data → Manage parameters → `DataFolder`* → set to the repo root,
   e.g. `C:\code\bank-marketing-powerbi`. Then **Refresh**.

   Every query builds its path from that one value, so this is the only thing you
   need to change.

Alternatively, edit `DataFolder` directly in
`Bank Marketing.SemanticModel/definition/expressions.tmdl` before opening.

---

## Data

| File | Rows | Source |
|---|---|---|
| `data/bank-additional-full.csv` | 41,188 | UCI Machine Learning Repository |
| `data/bank-additional-names.txt` | — | UCI's own column documentation |
| `data/BOU_Uganda_Monthly.csv` | 1,474 | Bank of Uganda open data portal |

**UCI Bank Marketing.** Moro, S., Rita, P. and Cortez, P. (2014). *Bank Marketing*
[Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5K306>.
Licensed **CC BY 4.0**. The file here is `bank-additional-full.csv` — semicolon
delimited, every text value quoted.

**Bank of Uganda.** Monthly interest and exchange rates pulled from the Knoema-hosted
open data portal at `cb-uganda.opendataforafrica.org` (no authentication required;
send a browser User-Agent). Six series: Central Bank Rate, commercial lending and
deposit rates, the overall interbank rate, and UGX/USD period-average and period-end.

Two honest notes about the Uganda data, both surfaced on the report:

- **The CBR series starts in July 2011**, because that is when Uganda adopted the
  Central Bank Rate under inflation targeting. Earlier months are genuinely absent,
  not missing.
- **Lending and deposit rates publish one month behind** the CBR and the exchange
  rate, which is why the "latest value" measures each find their own series' last
  observation rather than assuming a common one.

The campaign data (Portugal, 2008–2010) and the Uganda data (2005–2026) are
deliberately **not** related to each other. They sit on two disconnected date tables,
because forcing them onto one calendar would leave both mostly empty. Each table's
description says so.

---

## The model

9 tables, 46 measures, 6 relationships — all many-to-one, single-direction.

**Campaign star.** `FactCampaignContact` (41,188 rows, one per client contacted)
joined to `DimDate`, `DimJob`, `DimEducation`, `DimAgeBand`.

**Uganda star.** `FactUgandaIndicator` (1,474 rows, one per indicator per month)
joined to `DimUgandaMonth` and `DimIndicator`.

**Disconnected.** `DimFunnelStage` drives the targeting funnel via `SWITCH`, since
the stages are cumulative filters rather than a column in the data.

**`_Measures`** holds every measure. Folders are numbered so they sort in reading
order — see [`docs/measures.md`](docs/measures.md).

Two conventions worth knowing before editing:

- **Pinned headline measures.** The four Executive Overview KPIs use
  `CALCULATE(..., REMOVEFILTERS())` so clicking a bar or a table row cannot silently
  rewrite the headline. Charts stay fully cross-filterable; only the headline is
  pinned. Use `Total Contacts` (responsive) rather than `Clients Contacted` (pinned)
  anywhere a figure *should* follow the filters.
- **Deliberate blanks.** Measures return `BLANK()` rather than a misleading number at
  the edges — a spread is blank in months where either leg has not published, the
  first-to-last-year deltas are blank when only one year is in view, and the mm:ss
  duration is blank for months with no calls so empty rows drop out of tables.

---

## Validation

```bash
python tools/validate_pbip.py
```

Exit 0 means clean. It runs offline — no Power BI needed — and checks that:

- every visual field binding resolves to a real table, column or measure
- every relationship endpoint exists
- every measure has a description, a display folder and a format string (text and
  image-URI measures are exempt, by name, so a rename fails loudly)
- fact tables document their grain, the date table is marked, auto date/time is off
- **TMDL block indentation is legal** — a multi-line body must be indented deeper
  than its own property lines, or the parser folds `lineageTag` into the code and
  Power BI refuses the file
- the report theme declares `reportVersionAtImport`
- no page exceeds 8 *data* visuals, every visual has alt text, every page has
  navigation

Run it after any edit, and always after a rename.

---

## Notes for anyone hand-editing PBIP

Things that cost real time here, recorded so they cost you less:

- **`//` comments are rejected in `relationships.tmdl`** at any position or
  indentation. Put the note on the column instead.
- **A multi-line TMDL body must be indented deeper than its property lines.** Power BI
  writes expression bodies at two tabs with properties at one, and partition `source =`
  bodies at four tabs with properties at three. Match that.
- **Loading a model successfully does not mean it is valid.** An offline TMDL load will
  happily accept a file whose M is broken; it does not validate M at all. Desktop is
  the real check.
- **Unknown `queryState` roles and unknown format properties are silently ignored** —
  a wrong name never announces itself, the visual just renders without that binding.
- **The card visual auto-scales its text** to the container and ignores the `fontSize`
  in the JSON. Size cards by geometry, not font size.
- **Buttons ignore `text` and `outline` from PBIR** (only `fill` applies), so the
  navigation captions here are drawn by textboxes with a transparent button on top as
  the click target.
- **Desktop rewrites the whole project on save** and will overwrite on-disk edits made
  while it holds the file open. Either close it first, or edit the live model through
  the modeling API and export back.

---

## Licence

Code and report definitions: [MIT](LICENSE).

The UCI Bank Marketing dataset is © its authors under CC BY 4.0 and is redistributed
here under that licence with the citation above. Bank of Uganda figures are public
data from the Bank of Uganda open data portal. This project is a portfolio exercise
and is not affiliated with, endorsed by, or a product of any bank.

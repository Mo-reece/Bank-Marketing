# Measure reference

Generated from `Bank Marketing.SemanticModel/definition/tables/_Measures.tmdl`.
Every measure carries a description, a display folder and (unless it returns text
or an image URI) a format string; `tools/validate_pbip.py` enforces this.

## 01 Campaign Volume

| Measure | Format | What it is |
|---|---|---|
| `Subscriptions` | `#,0` | Clients who subscribed to the term deposit. |
| `Total Contacts` | `#,0` | Clients contacted in the campaign. One row per client, so this counts clients reached, not calls placed. |

## 02 Conversion

| Measure | Format | What it is |
|---|---|---|
| `Contacts per Conversion` | `#,0.0` | How many clients must be contacted to win one subscription. Lower is better; campaign-wide it is 8.9. |
| `Conversion Rate %` | `0.00%` | Share of contacted clients who subscribed. Campaign-wide this is 11.27%. |
| `Conversion Rate % (Prior Success)` | `0.00%` | Conversion rate among clients who already subscribed in a previous campaign. 65.11% campaign-wide - by far the strongest signal in the data. |
| `Conversion Rate by Previous Outcome` | `0.00%` | Conversion rate for a single previous-campaign outcome. Deliberately blank when more than one outcome is in context, so a total row can never be mistaken for a per-outcome rate. Use it broken down by Previous Outcome. |
| `Prior Success Lift` | `0.0"x"` | How many times better prior-success clients convert than the campaign average. Around 5.8x. |

## 03 Call Quality

| Measure | Format | What it is |
|---|---|---|
| `Avg Call Duration` | `#,0 "s"` | Mean length of the last call, in seconds. Only known after the call ends, so it explains outcomes rather than predicting them. |
| `Avg Call Duration (mm:ss)` | `-` | Mean call length formatted as minutes and seconds, for KPI cards and tables. Blank when no calls fall in context, so empty months drop out of a table rather than showing as ':'. |

## 04 Segment Analysis

| Measure | Format | What it is |
|---|---|---|
| `Conversion vs Campaign Average (pp)` | `+0.00%;-0.00%;0.00%` | Gap between this segment's conversion rate and the campaign average, in percentage points. Positive means the segment beats the average. |
| `Segment Share of Subscriptions` | `0.0%` | This segment's share of all subscriptions won. Shows where the volume actually came from, which is not always where the rate is highest. |
| `Subscriptions (Top Segments)` | `#,0` | donut stays readable. Blank for the rest. |

## 05 Uganda Banking

| Measure | Format | What it is |
|---|---|---|
| `Central Bank Rate` | `0.00"%"` | Bank of Uganda policy rate, monthly. The series starts in July 2011, when Uganda adopted the CBR under inflation targeting - earlier months are genuinely absent, not missing. |
| `Central Bank Rate (Latest)` | `0.00"%"` | Policy rate in the most recent month that has an observation, within whatever period is filtered. |
| `Deposit Rate` | `0.00"%"` | Weighted-average shilling deposit rate (7-12 month time deposits) paid by Ugandan commercial banks. |
| `Indicator Value` | `#,0.00` | Average observed value of the selected Bank of Uganda series over the months in context. Base measure for the named rates below. |
| `Interbank Rate` | `0.00"%"` | Overall interbank lending rate between Ugandan commercial banks. |
| `Lending Rate` | `0.00"%"` | Weighted-average shilling lending rate charged by Ugandan commercial banks. |
| `Lending Rate (Latest)` | `0.00"%"` | Commercial lending rate in the most recent month that has an observation. This series runs one month behind the policy rate. |
| `Lending Spread over CBR` | `0.00"pp"` | Gap between the commercial lending rate and the policy rate, in percentage points, averaged over the months in context. Blank before July 2011, when there was no CBR to compare against, and blank in the newest month, because the lending rate publishes one month behind the CBR. A persistent wide gap means policy cuts are not reaching borrowers. |
| `Lending Spread over CBR (Latest)` | `0.00"pp"` | Gap between the lending rate and the policy rate in the most recent month where both are published. |
| `Lending-Deposit Spread` | `0.00"pp"` | Gap between what banks charge borrowers and what they pay depositors, in percentage points. A standard read on banking-sector margin and competition. |
| `UGX per USD` | `#,0` | Market exchange rate, shillings per US dollar, at month end. A rising line means the shilling is weakening. |
| `UGX per USD (Latest)` | `#,0` | Month-end shilling rate against the US dollar in the most recent month with an observation. |

## 06 Report Support

| Measure | Format | What it is |
|---|---|---|
| `Campaign Window` | `-` | Campaign window in view, as a compact range like 'May 2008 - Nov 2010'. Same logic as Data Coverage Note without the sentence prefix, for narrow containers. Collapses to a single month when only one is in view. |
| `Data Coverage Note` | `-` | States the campaign window currently in view, so a filtered page never reads as if it covered the whole campaign. Blank when no campaign month is in context. |
| `Selected Segment` | `-` | Text label describing the current Job, Education and Age Band selection. Used as the drill-through page header so the reader always knows what they drilled into. |

## 07 Targeting Funnel

| Measure | Format | What it is |
|---|---|---|
| `Funnel Contacts` | `#,0` | Clients remaining after each cumulative targeting rule. Blank unless a single funnel stage is in context, so a total row can never be mistaken for a stage. |
| `Funnel Conversion Rate %` | `0.0%` | Conversion rate of the clients remaining at each funnel stage. Rises from 11.27% for the whole campaign to 66.89% for prior subscribers reached quickly on mobile. |

## 08 Executive Context

| Measure | Format | What it is |
|---|---|---|
| `Contacts (Final Year)` | `#,0` | Clients contacted in the last campaign year in view (2010 unfiltered). Reference figure for the headline contact count, showing where the campaign ended up rather than its total. |
| `Contacts per Conversion (Final Year)` | `#,0.0` | Calls needed per deposit won in the last campaign year in view. Lower is better. |
| `Conversion Change vs First Year (pp)` | `+0.0"pp";-0.0"pp";0.0"pp"` | Change in conversion rate from the first campaign year to the last, in percentage points (+47.3pp: 4.8% in 2008 up to 52.1% in 2010). Blank when only one campaign year is in view. |
| `Conversion Rate % (Final Year)` | `0.0%` | Conversion rate in the last campaign year in view (52.1% in 2010, against 11.27% for the campaign as a whole). |
| `Subscriptions (Final Year)` | `#,0` | Term deposits opened in the last campaign year in view (2010 unfiltered). |

## 09 Sparklines

| Measure | Format | What it is |
|---|---|---|
| `Sparkline Contacts` | `-` | Sparkline of contact volume by campaign month, rendered as an inline SVG for the card visual image slot. Blank if fewer than two months are in context. |
| `Sparkline Contacts per Conversion` | `-` | Sparkline of calls needed per deposit won, by campaign month, as an inline SVG for the card visual image slot. A falling line is an improvement. |
| `Sparkline Conversion Rate` | `-` | Sparkline of conversion rate by campaign month, as an inline SVG for the card visual image slot. Rising line shows the shift from volume to targeting. |
| `Sparkline Subscriptions` | `-` | Sparkline of term deposits opened by campaign month, as an inline SVG for the card visual image slot. |

## 10 Headline (pinned)

| Measure | Format | What it is |
|---|---|---|
| `Calls per Deposit` | `#,0.0` | Campaign-wide calls needed per deposit won, pinned against cross-filtering. |
| `Campaign Conversion Rate` | `0.00%` | Campaign-wide conversion rate of 11.27%, pinned against cross-filtering. |
| `Clients Contacted` | `#,0` | Clients contacted across the whole campaign, pinned so cross-filtering cannot change it. Use on the Executive Overview headline; use Total Contacts anywhere the figure should respond to filters. |
| `Contacts Change vs First Year %` | `+0.0%;-0.0%;0.0%` | Change in contact volume from the first campaign year to the last (-92.6%: 27,690 in 2008 down to 2,058 in 2010). Pinned against cross-filtering. |
| `Contacts per Conversion Change vs First Year %` | `+0.0%;-0.0%;0.0%` | Change in calls needed per deposit from the first campaign year to the last (-90.7%). Negative is an improvement. Pinned against cross-filtering. |
| `Conversion Lift vs First Year (x)` | `0.0"x"` | How many times higher the conversion rate is in the last campaign year than the first (10.8x). Pinned against cross-filtering. |
| `Deposits Opened` | `#,0` | Term deposits opened across the whole campaign, pinned against cross-filtering. |
| `Subscriptions Change vs First Year %` | `+0.0%;-0.0%;0.0%` | Change in deposits won from the first campaign year to the last (-19.9%). The pairing is the point: volume fell 93% while deposits fell only 20%. Pinned against cross-filtering. |

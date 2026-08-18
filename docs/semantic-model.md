# Semantic model

Generated from the TMDL in `Bank Marketing.SemanticModel/definition/`.
Measure detail lives in [measures.md](measures.md).

## Tables

### `DimAgeBand`

Client age grouped into six bands. Conversion is U-shaped across these: highest at both ends, lowest in mid-career.

*3 columns*

`Age Band`, `Age Band Sort`, `Life Stage`

### `DimDate`

Contiguous daily calendar, 2008-01-01 to 2010-12-31. Marked as the model date table. The campaign fact joins on the first day of its campaign month.

*9 columns*

`Date`, `Year`, `Month Number`, `Month`, `Year Month`, `Year Month Label`, `Year Month Sort`, `Quarter`, `Is Campaign Month`

### `DimEducation`

Highest education level reached. 8 members, ordered from lowest to highest attainment.

*3 columns*

`Education`, `Education Sort`, `Education Group`

### `DimFunnelStage`

Grain: one row per targeting-funnel stage. Disconnected lookup - no relationship to the fact. Each stage is a strict subset of the one above it, so the funnel is honest: 41,188 -> 26,144 -> 21,740 -> 18,246 -> 1,175. Labels are kept under 17 characters so they do not truncate in the funnel visual.

*2 columns*

`Stage Order`, `Funnel Stage`

### `DimIndicator`

The six Bank of Uganda series in the model: policy rate, commercial lending and deposit rates, interbank rate, and two UGX/USD measures.

*3 columns*

`Indicator`, `Category`, `Unit`

### `DimJob`

Client occupation. 12 members, sourced from the campaign fact.

*2 columns*

`Job`, `Job Group`

### `DimUgandaMonth`

Month calendar for the Bank of Uganda data, Jan 2005 - Jul 2026. Separate from DimDate because the two subject areas share no timeline and are never analysed together.

*6 columns*

`Date`, `Year`, `Month Number`, `Month`, `Year Month Label`, `Year Month Sort`

### `FactCampaignContact`

Grain: one row per client contacted in the campaign, describing that client's LAST contact. 41,188 rows covering May 2008 - November 2010 for a Portuguese bank's term-deposit telemarketing.

*25 columns*

`Campaign Month`, `Age`, `Age Band`, `Job`, `Education`, `Marital Status`, `Credit in Default`, `Housing Loan`, `Personal Loan`, `Contact Channel`, `Contact Day of Week`, `Contact Day of Week Sort`, `Call Duration (Seconds)`, `Contacts This Campaign`, `Days Since Previous Contact`, `Previous Contacts`, `Previous Outcome`, `Previously Contacted`, `Subscribed`, `Subscribed Flag`, `Employment Variation Rate`, `Consumer Price Index`, `Consumer Confidence Index`, `Euribor 3 Month Rate`, `Number of Employees`

### `FactUgandaIndicator`

Grain: one row per indicator per month. Bank of Uganda monthly statistics, Jan 2005 - Jul 2026. Unrelated to the Portuguese campaign data - it is a separate subject area on its own timeline.

*3 columns*

`Date`, `Indicator`, `Value`

### `_Measures`

Home for every explicit measure in the model. Holds no data.

*1 columns, 46 measures*

## Relationships

All many-to-one, single cross-filter direction, active.

| From (many) | To (one) |
|---|---|
| `FactCampaignContact.Campaign Month` | `DimDate.Date` |
| `FactCampaignContact.Job` | `DimJob.Job` |
| `FactCampaignContact.Education` | `DimEducation.Education` |
| `FactCampaignContact.Age Band` | `DimAgeBand.Age Band` |
| `FactUgandaIndicator.Date` | `DimUgandaMonth.Date` |
| `FactUgandaIndicator.Indicator` | `DimIndicator.Indicator` |

`DimFunnelStage` is deliberately disconnected: the funnel stages are
cumulative filters expressed in DAX, not a column in the fact table.

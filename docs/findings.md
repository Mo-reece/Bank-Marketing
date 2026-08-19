# Findings

Every figure below was computed against the refreshed model and cross-checked
against the source CSV independently in Python. Where a number appears as text on
the report, it is the same number.

## Campaign totals

| | |
|---|---|
| Clients contacted | 41,188 |
| Deposits opened | 4,640 |
| Conversion rate | 11.27% |
| Calls per deposit | 8.9 |
| Mean call duration | 258.3 s (4:18) |
| Campaign window | May 2008 - Nov 2010, 26 active months |

## The strategy shift

| Year | Contacts | Deposits | Conversion | Calls per deposit |
|---|---|---|---|---|
| 2008 | 27,690 | 1,339 | 4.84% | 20.7 |
| 2009 | 11,440 | 2,228 | 19.48% | 5.1 |
| 2010 | 2,058 | 1,073 | 52.14% | 1.9 |

Contacts −92.6%, deposits −19.9%, conversion x10.8, calls per deposit −90.7%.

The pairing is the whole story: **93% fewer calls cost only 20% of the deposits**.
2009 actually produced the most deposits of any year, on 41% of 2008's call volume.

## Targeting funnel

Each stage is a strict subset of the one above, so this reads honestly as a funnel.

| Stage | Clients | Conversion |
|---|---|---|
| All contacted | 41,188 | 11.27% |
| On mobile | 26,144 | 14.74% |
| ...within first 3 calls | 21,740 | 15.79% |
| ...no prior refusal | 18,246 | 16.01% |
| ...prior subscriber | 1,175 | 66.89% |

## Predictors, strongest first

**Prior campaign outcome** - the single strongest signal in the data.

| Previous outcome | Conversion |
|---|---|
| Success | 65.11% |
| Failure | 14.23% |
| Not previously contacted | 8.83% |

A prior subscriber converts at 5.8x the campaign average.

**Contact intensity** - conversion falls monotonically with the number of calls
made in this campaign.

| Calls | Conversion |
|---|---|
| 1st | 13.04% |
| 4th | 9.39% |
| 11th or later | 3.11% |

Repeated calling does not wear prospects down, it burns them.

**Channel** - mobile converts at 2.8x landline.

| Channel | Contacts | Conversion |
|---|---|---|
| Cellular | 26,144 | 14.74% |
| Telephone | 15,044 | 5.23% |

**Occupation** - a wide spread, and note the split between rate and volume.

| Job | Conversion | Deposits |
|---|---|---|
| Student | 31.43% | 275 |
| Retired | 25.23% | 434 |
| Unemployed | 14.20% | 144 |
| Admin | 12.97% | 1,352 |
| Blue collar | 6.89% | 638 |

Admin staff convert at a middling 13% but supply **more deposits than any other
occupation** - the best rate and the biggest source are different segments, which is
why the Executive Overview shows share of deposits rather than rate alone.

**Age** - conversion is U-shaped, strongest at both ends of life.

| Age band | Conversion |
|---|---|
| 65+ | 47.21% |
| Under 25 | 23.97% |
| 55-64 | 13.57% |
| 25-34 | 12.17% |
| 35-44 | 8.65% |
| 45-54 | 8.65% |

## Caveat that matters

`duration` - call length - is the strongest single correlate of subscribing, but it
is only known **once the call has ended**. It explains outcomes; it cannot be used to
choose who to call. The report says so on the page rather than quietly ranking it as
a predictor.

## Uganda banking context

A separate, unrelated dataset, kept on its own disconnected calendar.

| | |
|---|---|
| Central Bank Rate, latest | 9.75% |
| Peak CBR | 23.0% (Nov 2011) |
| Trough CBR | 6.5% (Jun 2021) |
| Commercial lending rate, latest | 16.93% |
| Lending spread over CBR, latest | 7.18pp |
| Mean lending spread since 2011 | 9.68pp |
| Widest spread | 13.93pp (Jul 2020) |
| UGX per USD, latest (month end) | 3,751.84 |

Policy rate cuts only partly reach borrowers: the gap between the lending rate and
the policy rate has averaged nearly 10 percentage points since 2011.

# MLB rest-day observational analysis

`get_data.py` downloads public MLB box scores and derives player-game batting average (hits / at-bats). A player is classified as rested when more than one calendar day has passed since that player's previous game appearance in this extract. `analysis.py` pairs each rested observation with the nearest observation of the same player after consecutive-day appearances, within 30 days; controls may be reused. It reports the mean paired difference and a naive pair bootstrap interval.

```sh
python get_data.py --start 2024-04-01 --end 2024-04-14 --out observations.csv
python analysis.py observations.csv
python -m unittest -v
```

The committed extract covers April 1–14, 2024, with 3,237 eligible player-game observations. It contains 840 matches and 66 unmatched rested observations. The mean difference is -0.0074 hits per at-bat, with a naive 95% bootstrap interval of [-0.0283, 0.0145]. This is an exploratory association, not a causal estimate: player selection, injuries, pitcher quality, park, lineup decisions, repeated observations and reused controls can confound the result or invalidate the naive interval. Rest is measured between game appearances, not confirmed team rest days; the first observed appearance is omitted. A longer window, richer covariates, pre-specified design, overlap checks and player-clustered inference are needed before causal conclusions.

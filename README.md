# Runescape market data scraping

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

This code provides a means for extracting historic pricing data from the runescape wikipedia

## Data collected

All data is sourced by runescape.wiki (on a daily basis) from the Runescape Grand Exchange and 
stored on the wiki.  These python scripts extract the data, which currently comprises price data 
and trade volume data. The latter seems to be largely unavailable since Jan 2019.

## Running the script

There are two optional parameters that can be specified:

1) **--start-date**  - by default, the script will only process data from the previous month end, but can 
upload more historic data based on the given start date
2) **--refresh-assets** - the script can also download refreshed list of assets from the rune wiki to 
help capture newly added assets

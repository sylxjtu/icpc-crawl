# ICPC Outstanding Teams Display

Use it to show what team had participated ICPC regional contest more than twice a year

## Data source

https://icpc.baylor.edu

Usually the data is updated when all regional contests has ended, so don't be suprised when you found there's no data about recent contests.

## Requirement

Python 3

## Usage

```bash
# Year means Year-1 to Year, For example, 2018 means 2017-2018
YEAR=2019

py -3 -m pip install scrapy
py -3 -m scrapy crawl contest_list -a year=$YEAR
py -3 process.py $YEAR
```

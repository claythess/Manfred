# Manfred
Meta Analytics Network, Full Reference Esoteric Database

This allows for seamless creation of esoteric stats, and allows one to quickly generate leaderboards for new and existing stats

# Usage

## Running manfred.py
To run as interactive REPL shell
```
python3 manfred.py -r
```
To run file, e.g. TTO.txt
```
python3 manfred.py -f TTO.txt
```


## Stat creation
```
let new_stat = ERA - SO * IP

let other_stat = (OBP - AVG) * BB

let yet_another_stat = other_stat * ISO
```
You can put variable names in quotations, to save Absolute strings. This helps with stats like ERA+, or HR/FB%+, which otherwise contain math tokens
```
let some_stat = "K%+" + "BB%+"
```
## Outputting stats
```
show output_type [year] (PARAM1, PARAM2) top 10 PARAM_TO_SORT_BY
```
Where output_type is pitching, batting, qpitching (qualified pitchers), qbatting (quallified batters), apitching (aggregate all years pitching), abatting (aggregate all years batting)

```
show output_type [from_year, to_year] (PARAM1, PARAM2, NEW_PARAM) top 10 PARAM_TO_SORT_BY

show output_type [year] (PARAM1, PARAM2, PARAM3) PARAM2 < 5, PARAM3 = VALUE, top 10 PARAM
```
PARAM3 here can compare any attribute to be less than, greater than, or equal to a value. These can be chained together by seperating conditions with a comma

## E.g.
```
let esoteric_pitching = IP - (HR * 13) - (BB * 3) + (SO * 5)

show pitching [2023] (Name, Team, esoteric_pitching) IP > 50, W > 1, top 10 esoteric_pitching
```
Output: 
```
Name              | Team  | esoteric_pitching | 
Spencer Strider   | ATL   | 1479.2            |
Blake Snell       | SDP   | 1452.0            |
Kevin Gausman     | TOR   | 1288.0            |
Dylan Cease       | CHW   | 1237.0            |
Gerrit Cole       | NYY   | 1203.0            |
Pablo Lopez       | MIN   | 1196.0            |
Kodai Senga       | NYM   | 1186.1            |
Zac Gallen        | ARI   | 1165.0            |
Sonny Gray        | MIN   | 1160.0            |
Charlie Morton    | ATL   | 1145.1            |
```

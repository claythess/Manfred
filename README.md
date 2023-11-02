# Manfred
Meta Analytics Network, Full Reference Esoteric Database

This allows for seamless creation of esoteric stats, and allows one to quickly generate leaderboards for new and existing stats

# Installation

Install repo w/ Git:
```
git clone git@github.com:claythess/Manfred.git
```
Install dependencies
```
pip install -r requirements.txt
```

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
To run mafnred with colored output
```
python3 manfred -r -c {color}
```
where color is "default", "night", "wine", "eggshell", "oceanic", "forest", or "america". If no value is supplied, -c will use the "default" color theme

Do feel free to add your own themes in the Manfred/Executor.py file

I should note I encountered a bug where stats that obviously exist, like 'Name' were being reported as not existing, 
the solution I found to this (without much looking) was updating all your site packages, which is a bit nuclear, but at least a fix.
https://www.activestate.com/resources/quick-reads/how-to-update-all-python-packages/

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

One can also use builtin variable lists "basic" and "statcast"
```
show pitching [2020] (Name, basic) Team = CHW, bot 5 ERA
show abatting [2020, 2022] (Season, Name, statcast) top 10 "wRC+"
```
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

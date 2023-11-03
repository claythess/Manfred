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

## Notes from teh author

The first time you retrieve data for any given year, expect a delay, as the database is downloading. Data caching is builtin, so subsequent queries will be much faster

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

All database stats can be found in the PitchingCommands.txt and BattingCommands.txt files. These commands are case sensitive.
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
```
let dumb_bases = SB - CS * 5 - GDP * 10
let useless = dumb_bases * AVG

show apitching [2020, 2023] (Name, dumb_bases, useless, basic) OPS > 0.700, top 10 dumb_bases

Name                  | dumb_bases | useless  | HR  | AVG   | OBP   | SLG   | OPS   |
----------------------|------------|----------|-----|-------|-------|-------|-------|-
Byron Buxton          | -34.0      | -8.228   | 77  | 0.242 | 0.309 | 0.534 | 0.844 |
LaMonte Wade Jr.      | -70.0      | -17.08   | 43  | 0.244 | 0.342 | 0.422 | 0.764 |
Cavan Biggio          | -79.0      | -17.933  | 30  | 0.227 | 0.338 | 0.375 | 0.713 |
Joey Gallo            | -83.0      | -15.023  | 88  | 0.181 | 0.315 | 0.416 | 0.731 |
MJ Melendez           | -87.0      | -19.749  | 34  | 0.227 | 0.314 | 0.396 | 0.71  |
Jazz Chisholm Jr.     | -101.0     | -24.745  | 53  | 0.245 | 0.304 | 0.452 | 0.756 |
Mike Trout            | -109.0     | -30.738  | 83  | 0.282 | 0.384 | 0.584 | 0.968 |
Adam Duvall           | -111.0     | -25.641  | 87  | 0.231 | 0.288 | 0.487 | 0.775 |
Brandon Lowe          | -117.0     | -28.197  | 82  | 0.241 | 0.334 | 0.481 | 0.815 |
Brandon Marsh         | -119.0     | -30.821  | 25  | 0.259 | 0.33  | 0.406 | 0.736 |

```
```
                            .     . .                                                                                        
                 .   .... . .......... .............---,,,,!!!!!!!!!!!!!!!,,,,,--.       .                                   
            ..   ... ... ....... .......--,,,,!!!!7?JIC333&3CCVIIJJIIICCCCIJJJJJJ?!,,-..    . ........  .                    
 .     .... .... ....................--,,!!!!7?JJIYVCCCCCC3&&&3CCCVYIIIIIIJIJJ?7?JJIJ7!,,-............... .... . ..... .     
  ..  .. ......     ...       .....--,,,,,,!!7JYC3L2PG9ZZ4GGGGG002&3CCCVIVIJJ?JJ7777?JJ17!!,,-...........................    
....          . ..     .--,,,!!!!,,,,!!!7JICCCCVVVIJJIIIVVVCCCCC33CCCCCVIIJJ?777!!!77777!!!!!!,,---.-........................
. .. ... ..      .-,,!7JJJJJ7!!!!7?JC&2044Z94S0P222&&&5233&&L3333CCVVYIVYJ??1JJ7!!!!!!7!!!!!!!!,,,,--........................
...........  .-,!1VCCIJ7!!!!7JC3P4ZZZZZDDZDDDDDDDDDDDDDDDDDDDDKZ40F2&3CCCVYI???177!!!!!!!!!!!!,!,,,,,,--.....................
........  .-,!VCCVJ7!!!!!JC2SGZKKDDDDDDDDDDH8QQDDDDDDDDDDDHDHDDDDZS0OF2&&333CCVVVIJ7!!!,,,,,!!!,,,,,,,,,--...................
........-,!JIC33VIJJJI3049ZDDDH8DDDDDDDDDDDDDDDDDDKZZZZZ49X44440OOPPPFLL5&333CCCCCCVIJ7!!,,,--,,,,,,---,,,,--................
......--,7JVVVC33332O4ZZDKDDHDKDDDDKDKKDZKDDDKKKZZZZX994GGG4G0PPPF2222L52&333CCCCCCCVIJ??7!!!,,,,,,,---,,,,,----.............
......-!777JJJC&200GGG49DDDDDDDDDDDDDDDZKDDKZKZX44449944GS00000PFPOOOPFFPL333CCCCCCCIIIJ7777J17!!!!!,,,,,,-,,,---............
.....-,77?JV3LPP204X44XZDDDDDDDDDDDDDDKKKZKKZZX99494494SGGSG40GGOP00OOP2253CC3CCCCCVIIIJJ7777JJ?!!!!7!!,,,,----,----.........
...---!7VC32S9GL20444XZZDDDDDDDDDDDDDDDDDZZZ44G49444G0S4994G444G0SGGG0P2525333CCCCCVVIIJ?7!!!77??77!7?!,,,,,,,-,----.........
..--,,!I3C&O0233P4444ZXXKDDDDDDDDDDDDDDKZZZ4X444ZX440POZZ94G44GSGSGGOF2222222&33CCCYIIJ17!!!!7777777!17!,,!,,,,,-............
.-,,,,JCVCL223&PO4404XXXZKKDDDDDDDDDKKDZXZZX44GG944GGG4ZX44GGGGGG4GP22522&&&&33CCCVIJJ?77!!7777!777!!!!!,,,,,,,,---..........
-----!3CY3&253320O0OOGG4XZXZZZKKDDDKKKZZZZX444G094G044Z9X9GG4449X902F2222L&33CCIIJJIJJ177777777!!!!!!!!,,,,,,,,,,,-..........
-.--,?CJV3&22&352O0PPPP0499ZZZZZZZKZZXZZZZ9444G0SGG0GGG4994X49ZZ9G0PF2&3&3CCVIJJJJJJ??77777777!!!!!!,,!,,,,,,,!!!,---........
...--7J?C33322L&&2PO222G4ZZX9ZZZDDDKZZ4XZZZ94944S0PP25GZZZZZZZZ9944O23&L&33C33CCCYJJ?77!!!!7!!!!!!!,,,,,,,,,,,,!!,,-.........
.....,!JIVC3L225&332&33PS444449ZDDKZZZ949X44SG4GGS0022ZKZZZZZXX94GO2222253CVIJJ7!!!777!!!!!!!!!!!!,,,,,,,,,,,,,,!!,-.........
.....-,7JJCC3&L3CCCIJ!!!!7!!!!!!7JIIVCF0GX4GOOPF444440ZKZZZZXX4S2CVJJ77!!,,,-------,,,!!!!!!!!!!,,,,,,,,,,,,,,,,,!!,--.......
......-!JJICCC3CCCC17!,,,,,,,,,,,,!!!!JYC&&&&&354O04GPGG0P2&3CYJ!,,,,--. ..-,,,,,,,,,,,!!!!!!!!,,,,,-,,,,,,,,,,,,!!,,,,......
..... ,J?1JYVCCCCCVYIIJJJJJJ17!!!!!!7777JIIVCCCL3&2L333&3CIJ?7!,,,,,-----,,,!!!!!!!!!!!,,,,!!,,,,,,,,,,,,,!,,,,,!,,-.-,-.....
.....-!3VJJIVCCCCIVCVCCCCVJ77!!!,,,!!!!!!!7JIVCC35P23CCVI7!!,,--,,,,,,,,,!!,,,,,,,!!,,,,,,,!!,,!,,,,,-,,!!!,,,,,,----,!-.....
......-!VVIIVCCCYJJJ117!!,,!!7?JJ?7!!!!!!!!!!7JV3P4X2CJ7!,,---,,,,,!7777777!!!!!!,,,,,,,,,,!!,,,,,,,,,,,!,,,,!,,,!!,!J!-.....
........!33IIC33VIJ77!!!!7VCCJ7!!!!!!!!!!!!!!7?I54ZZPCVJ!,,,,,,,,!7!!7,,--  ..----,,!!,,!!!!,,,,,,,,,,,,,,--,!,,!77!,!!-.....
........,C3IIC3&&CVIJJJI7!,,!7!--..-,-!!,!!7JCJCG44G233V7!,,!77!,,,7C2C!,,,,,,!!,,,,!!!!777!!!!,,,,,,,----,-,-.,!!7!!!,-.....
....-...,C3IJC&3&2L3&3L2VJ?JVCCJ!!!!77JJ7JIC&5C24X94053V7!!!!7?77!!77?JJJ?7!!!!!!!!77?17?J77!!!!,,,,,,,---,!- -,!!!7?J!,.....
-..---.-V23YJC3L2PSS00G4423CCVVIIYJJJ?7?JJVC3&&F4ZKZG&V1!!!!777!!!!!!!!!77777771JIVCCCCIJJ77!!!!,,,,,,,---,J7,!1J777?J!-.....
------.-2X&CJVC35F4ZXZKZX4S2L33CCVYIIIVC3&PS0PL0XZKZ4PCJ!!!7JJJJ177777777?JJICC3&L55L3CIJ177!!,,,,,,,-,---,7J!!!7!!!7!,-.....
--------7425VIC3LP4XZZDDDDKZX4S0OPO0G4ZZZ9X4GO0XZZX00P&VJ7!!7J1JJVVIVVVVYIIV3&LL&&3CYJJJ??7!!!,,,,,,,,,---,77,,!7?!,,,--.....
---------IKGVJIC32PS44XZKKDDDKZZKKDKKKDDZG0SO2O9ZZ4G0F&CJ7!,!!!!7JVC333C33333&333CVIJ???7777!!!,,,,,,,,---,!!7777!,,,,--.....
--------.!ZK2IIJC332PP049ZZKDDDDDDDDDDX02L2GFL20DKZ4GF3CJ!!!!117!777?JICC3&33333CVYIJ177777!!!!,,,,,,,,---,!7777!,,,---------
----------?04VVII322F22PS49ZZDDDDZX053C3L&2OL33LPOP233V?!!,,,!!!,,!J77!!7?JIVCCVYIIIJJ77!!!!!!,,,,,,,,,,--,?J?!!,,-----------
-----------!G&ICVC352P55204ZZKZ4O5CVCC2SGCJ?!,,!!??7!!!,,.   -,,,!?IIIJJ7!!!77?JJJJ?777!!!!!!,,,,,,,,,,,,--,!!,,-------------
------------,7JYCCC3&L&522O0G0F&CCC3P4ZKZ93J!!71J7!!,,----,,,!!7?JJJIIIJJJJ77!7777777!!!!!!!,,,,,,,,,,,,,--------------------
------------..!IVCC3&2&&552PF&3CC&P4XS4449402&3333CJ77?JJJJ??77??1J?777??1JJ177JJJ?7!777!!!,,,!,,,,,,,,,,--,-----------------
---------------7JVCC3L5&3522L33C3FSG02P0O22F5&&333CVVCCCCCCVJ1777?J77!77!!!71J1ICCVJ7!?77!!,,!,,,,,,,,,,,--------------------
---------------,?JVVC333&22&&5&&PP&33333&5L525&&5&3&3&3CCVIJ7!!!!!!!!!!!!!!771JC003V?!717!!,!!,,,,,,,,,,---------------------
----------------,JJJVC&3352F0O225CCIJJIJJ77!!!!7777777!!!,,,,,,,,,,,,,,,,!!!!7I3SO3V?!!?7!!!!!,,-,,,,,,----------------------
-----------------,?JJY33C32P4GPL3IJ17JIIJJJIV35POP22&333CCCYIVIJ?77!7!777777?I&GS23J7!!77!!!!,,,,,,,,----..,!-.--------------
-------------------!1IYCCC&2OS0F&CVC3&LL&3CCCCCCCCJJJ1?7!!!!!!!!!!!!777??JJJICLO23V1!!!!!!!!,,--,,,----...-!CV,  .-----------
--------------------,!?ICCC35FO23&P000OP2&3CIJ77!!!!7!!!!!!!!!77????JJJJJJJICC3&3CJ7!!!!!!,,,----..---.---,V2ZO,   .---------
-----------------------,!ICVC3333&2OS0PPOOFL3CCCC3F22P223CCCYIVCCCCCVYYYVVIIVVVCVJ7!!!!!!,,,---..-----,,-,7&9K27      .------
!!!!!!!!!!!!!!!!!!!!!!!,!!VVIIVC3L2P00G44G44XZZZZZZ940OO23CVC3&&&L&3CVIIJJJJ1J??7!!,,!!,,,--.. --,-,,!!-,J324&2J         .---
DDDDDDDKDDKKKKKKKKKKKKKKKZK4CJJJC&52FPOSGG4ZZ4GGOF533CC333CVVCCCCCVIIJ17777!!!!!!,,,,,,,--....-,,,,!!,,!S23OC&Z,             
@@@@@@@@@@@@@@@@@@@@@##NNNNE@Z3JJIVC33&&&FOOSO2L3CCVVYVYVVJ?7?JJJIIJ?7!!!!!!,,,,,,,------..--,,!!!7!!7OQL3PC3DI              
FFPPPPPOOOO0000SSSGGG44444449ZZF17!7777JJC333CCCCCCCIIJ7!!77!!7J1JJ7!!,,,,,,,-----...-----,,!!!!7!!!2@DC32V5KC-              
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,7?77!!,!!!777771?77!!!!!!!!!!!!!!,,,,,,,,-----,,---,,,,!!!!!!77!,?DNXV&&I2XC,               
...................-..-.--------.,JIJJJ7!!!!!!!!!!!!!!,!!!!!!,,,,,,,,,------,,,,,,,,,,!!77!!!!!!!VQ@OV23YOPCJ                
....--...-----------------------,5CJIIIVCI77!!!!!!!!777777!!!,,,,--------,,,,,,,,,,!!7777!!!!!!J3883V2CC03VL,                
.......-...-...------------,,---3M2JIIYVVCVJ?1???1J?7!!!,,,,,-----,,,,!!!!!!!!!!!!7??777!!7!!ILLHDCC5I3GCCGJ                 
.......-..---------------------!E@DIIVCCVCCCJJJJIYVCCC?!,,,,,,,!!!77?11?77777!!77?JJ?77777!79DOH4IC3Y2OC3ZV-                 
....--------------------------,ZE#S,!ICCCCCCCYJJIIVVCCCI?7!!!!!7?1JJ?J?7777777777???7777773EH0Z3JCCV0LVPZV,                  
---------------------------,--JRWQJ7,,IC333C33CIJJIIYVCCCVIJJ?77JJIJJJ1????777777?JJ?77?CQMZ24CJCICOCCX4V!.                  
-----------------------------,8BRPJC7,,1C333CCCCCVJJJIICCCVIJJJ1JJJJJJJJJJ?7!!!7JIIJ?7VDWR02PIYCI52VLKPVY-                   
-------------------,---------IWB@3&Y1V,-!V33333CCCVIJJJJVVVYJJJJ??7?JJJJJ??7!!?JJJJJCP@M#PF2JCVIP3VSZ33P!                    
------------------,---------,@BB@GZ3II!,-!?V3&&&33CCCVVVIVJ11?777771JJJJJ777!7JVC3523J!77L4JCVVPVCZOCPKY                     
--------------------,------.CBBM@@D5C3IJ,-,!7JC&222&33CCCCJ!7II777JJIIJJICCC3322&33CCVI?7!YOVI5Y3X3CZDC-                     
-----------------------....!QC7!JZ@44ZCCJ!-,!!7JV52P22&3CCC7?VCY1?JICVJ30PP53CC3333CVIIJJJ?3G&I2SC3KZC!                      
-----------------------....LFJ77!!!4E@ZQ0C!-,,!!7JC5PFF2&3CJIICCIICCCLZ9L3CCCCCCCCCCC3CCO55239K4I&DOV3,                      

```

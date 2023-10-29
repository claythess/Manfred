## Manfred
Meta Analytics Network, Full Reference Esoteric Database
This allows for seamless creation of esoteric stats, and allows one to quickly generate leaderboards for new and existing stats

## Usage

# Stat creation
let new_stat = ERA - SO * IP
let other_stat = (OBP - AVG) * BB

# Outputting stats
show [year] (PARAM1, PARAM2) top 10 PARAM_TO_SORT_BY
show [from_year, to_year] (PARAM1, PARAM2, NEW_PARAM) top 10 PARAM_TO_SORT_BY

# E.g.
let esoteric_pitching = IP - (HR * 13) - (BB * 3) + (SO * 5)
show pitching [2023] (Name, Team, esoteric_pitching) top 10 esoteric_pitching
Output: 

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

STATES = {
    "ALABAMA":	"AL",
    "ALASKA":	"AK",
    "ARIZONA":	"AZ",
    "ARKANSAS":	"AR",
    "CALIFORNIA":	"CA",
    "COLORADO":	"CO",
    "CONNECTICUT":	"CT",
    "DELAWARE":	"DE",
    "FLORIDA":	"FL",
    "GEORGIA":	"GA",
    "HAWAII":	"HI",
    "IDAHO":	"ID",
    "ILLINOIS":	"IL",
    "INDIANA":	"IN",
    "IOWA":	"IA",
    "KANSAS":	"KS",
    "KENTUCKY":	"KY",
    "LOUISIANA":	"LA",
    "MAINE":	"ME",
    "MARYLAND":	"MD",
    "MASSACHUSETTS":	"MA",
    "MICHIGAN":	"MI",
    "MINNESOTA":	"MN",
    "MISSISSIPPI":	"MS",
    "MISSOURI":	"MO",
    "MONTANA":	"MT",
    "NEBRASKA":	"NE",
    "NEVADA":	"NV",
    "NEW": "HAMPSHIRE"	"NH",
    "NEW": "JERSEY"	"NJ",
    "NEW": "MEXICO"	"NM",
    "NEW": "YORK"	"NY",
    "NORTH": "CAROLINA"	"NC",
    "NORTH": "DAKOTA"	"ND",
    "OHIO":	"OH",
    "OKLAHOMA":	"OK",
    "OREGON":	"OR",
    "PENNSYLVANIA":	"PA",
    "RHODE": "ISLAND"	"RI",
    "SOUTH": "CAROLINA"	"SC",
    "SOUTH": "DAKOTA"	"SD",
    "TENNESSEE":	"TN",
    "TEXAS":	"TX",
    "UTAH":	"UT",
    "VERMONT":	"VT",
    "VIRGINIA":	"VA",
    "WASHINGTON":	"WA",
    "WEST": "VIRGINIA"	"WV",
    "WISCONSIN":	"WI",
    "WYOMING":	"WY",
}

ELECTION_CANDIDATES = {
    "republican": [
        "jeb bush",
        "donald trump",
        "ben carson",
        "ted cruz",
        "marco rubio",
        "carly fiorina",
        "lindesey graham",
        "mike huckabee",
        "rand paul",
        "rick perry"
        "chris christie",
        "rick santorum",
        "scott walker",
    ],
    "democrat": [
        "joe biden",
        "hillary clinton",
        "bernie sanders",
        "jim webb",
        "lincoln chafee",
        "martin o'malley"
    ],
    "independent": [],
}
CANDIDATES = [item for sublist in ELECTION_CANDIDATES.values() for item in sublist]
PARTIES = [(party, party) for party in ELECTION_CANDIDATES.keys()]
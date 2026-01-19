"""North American countries lottery configuration"""

from typing import Dict, List


class CountryConfig:
    """Configuration for a country's lotteries"""

    def __init__(self, code: str, name: str, timezone: str, lotteries: List[Dict]):
        self.code = code
        self.name = name
        self.timezone = timezone
        self.lotteries = lotteries


# North American countries lottery configuration
NORTHAMERICA_COUNTRIES = [
    # United States
    CountryConfig(
        code="US",
        name="United States",
        timezone="America/New_York",
        lotteries=[
            {
                "name": "Powerball",
                "slug": "us-powerball",
                "url": "https://www.powerball.com/previous-results",
                "type": "selenium",
                "schedule": "59 3 * * 2,4,7",  # Mon, Wed, Sat 10:59 PM ET = 3:59 AM UTC
                "description": "Multi-state lottery across 45 states, DC, Puerto Rico, USVI",
            },
            {
                "name": "Mega Millions",
                "slug": "us-megamillions",
                "url": "https://www.megamillions.com/winning-numbers",
                "type": "selenium",
                "schedule": "0 4 * * 3,6",  # Tue, Fri 11 PM ET = 4 AM UTC
                "description": "Multi-state lottery across 45 states, DC, USVI",
            },
        ],
    ),
    
    # Canada
    CountryConfig(
        code="CA",
        name="Canada",
        timezone="America/Toronto",
        lotteries=[
            {
                "name": "Lotto 6/49",
                "slug": "ca-lotto649",
                "url": "https://www.olg.ca/en/lottery/play-lotto-649.html",
                "type": "selenium",
                "schedule": "30 2 * * 4,7",  # Wed, Sat 9:30 PM ET = 2:30 AM UTC
            },
            {
                "name": "Lotto Max",
                "slug": "ca-lottomax",
                "url": "https://www.olg.ca/en/lottery/play-lotto-max.html",
                "type": "selenium",
                "schedule": "30 2 * * 3,6",  # Tue, Fri 9:30 PM ET = 2:30 AM UTC
            },
        ],
    ),
    
    # Mexico
    CountryConfig(
        code="MX",
        name="Mexico",
        timezone="America/Mexico_City",
        lotteries=[
            {
                "name": "Melate",
                "slug": "mx-melate",
                "url": "https://www.pronosticos.gob.mx/",
                "type": "selenium",
                "schedule": "3 3 * * 4,7,1",  # Wed, Sat, Sun 9 PM CST = 3 AM UTC
            },
            {
                "name": "Chispazo",
                "slug": "mx-chispazo",
                "url": "https://www.pronosticos.gob.mx/",
                "type": "selenium",
                "schedule": "3 3 * * *",  # Daily 9 PM CST = 3 AM UTC
            },
        ],
    ),
    
    # Guatemala
    CountryConfig(
        code="GT",
        name="Guatemala",
        timezone="America/Guatemala",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "gt-loteria-nacional",
                "url": "https://www.leidsa.com/",
                "type": "bs4",
                "schedule": "0 2 * * 0",  # Sunday 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # Belize
    CountryConfig(
        code="BZ",
        name="Belize",
        timezone="America/Belize",
        lotteries=[
            {
                "name": "Boledo",
                "slug": "bz-boledo",
                "url": "https://www.boledo.bz/",
                "type": "bs4",
                "schedule": "0 2 * * 3,6",  # Wed, Sat 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # Honduras
    CountryConfig(
        code="HN",
        name="Honduras",
        timezone="America/Tegucigalpa",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "hn-loteria-nacional",
                "url": "https://www.loteriahonduras.hn/",
                "type": "bs4",
                "schedule": "0 2 * * 0",  # Sunday 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # El Salvador
    CountryConfig(
        code="SV",
        name="El Salvador",
        timezone="America/El_Salvador",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "sv-loteria-nacional",
                "url": "https://www.loteria.gob.sv/",
                "type": "bs4",
                "schedule": "0 2 * * 0",  # Sunday 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # Nicaragua
    CountryConfig(
        code="NI",
        name="Nicaragua",
        timezone="America/Managua",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "ni-loteria-nacional",
                "url": "https://www.loteria.gob.ni/",
                "type": "bs4",
                "schedule": "0 2 * * 0",  # Sunday 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # Costa Rica
    CountryConfig(
        code="CR",
        name="Costa Rica",
        timezone="America/Costa_Rica",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "cr-loteria-nacional",
                "url": "https://www.jps.go.cr/loteria-nacional",
                "type": "selenium",
                "schedule": "0 2 * * 0",  # Sunday 8 PM CST = 2 AM UTC
            },
        ],
    ),
    
    # Panama
    CountryConfig(
        code="PA",
        name="Panama",
        timezone="America/Panama",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "pa-loteria-nacional",
                "url": "https://www.loteria.gob.pa/",
                "type": "selenium",
                "schedule": "0 1 * * 3,0",  # Wed, Sun 8 PM EST = 1 AM UTC
            },
        ],
    ),
    
    # Cuba
    CountryConfig(
        code="CU",
        name="Cuba",
        timezone="America/Havana",
        lotteries=[
            {
                "name": "Lotería Nacional",
                "slug": "cu-loteria-nacional",
                "url": "https://www.loteria.cu/",
                "type": "bs4",
                "schedule": "0 5 * * 7",  # Sunday midnight EST = 5 AM UTC
            },
        ],
    ),
    
    # Jamaica
    CountryConfig(
        code="JM",
        name="Jamaica",
        timezone="America/Jamaica",
        lotteries=[
            {
                "name": "Supreme Ventures Lotto",
                "slug": "jm-lotto",
                "url": "https://www.supremeventures.com/lotto/results",
                "type": "selenium",
                "schedule": "0 3 * * 3,6",  # Wed, Sat 10 PM EST = 3 AM UTC
            },
            {
                "name": "Cash Pot",
                "slug": "jm-cashpot",
                "url": "https://www.supremeventures.com/cashpot/results",
                "type": "selenium",
                "schedule": "0 4 * * *",  # Daily 11 PM EST = 4 AM UTC
            },
        ],
    ),
    
    # Haiti
    CountryConfig(
        code="HT",
        name="Haiti",
        timezone="America/Port-au-Prince",
        lotteries=[
            {
                "name": "Loterie de l'État Haïtien",
                "slug": "ht-loterie-etat",
                "url": "https://www.loteriehaiti.ht/",
                "type": "bs4",
                "schedule": "0 5 * * 0",  # Sunday midnight EST = 5 AM UTC
            },
        ],
    ),
    
    # Dominican Republic
    CountryConfig(
        code="DO",
        name="Dominican Republic",
        timezone="America/Santo_Domingo",
        lotteries=[
            {
                "name": "Leidsa Quiniela Pale",
                "slug": "do-leidsa-quiniela",
                "url": "https://www.leidsa.com/",
                "type": "selenium",
                "schedule": "0 1 * * *",  # Daily 8 PM AST = 1 AM UTC
            },
            {
                "name": "Loteka",
                "slug": "do-loteka",
                "url": "https://www.loteka.com.do/",
                "type": "selenium",
                "schedule": "0 2 * * 3,6",  # Wed, Sat 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Bahamas
    CountryConfig(
        code="BS",
        name="Bahamas",
        timezone="America/Nassau",
        lotteries=[
            {
                "name": "Numbers",
                "slug": "bs-numbers",
                "url": "https://www.bahamaslottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 3,6",  # Wed, Sat 9 PM EST = 2 AM UTC
            },
        ],
    ),
    
    # Trinidad and Tobago
    CountryConfig(
        code="TT",
        name="Trinidad and Tobago",
        timezone="America/Port_of_Spain",
        lotteries=[
            {
                "name": "NLCB Play Whe",
                "slug": "tt-playwhe",
                "url": "https://www.nlcb.co.tt/play-whe",
                "type": "selenium",
                "schedule": "0 15,19,23 * * *",  # Daily at 10:30 AM, 2:30 PM, 6:30 PM AST
            },
            {
                "name": "Lotto Plus",
                "slug": "tt-lottoplus",
                "url": "https://www.nlcb.co.tt/lotto-plus",
                "type": "selenium",
                "schedule": "0 2 * * 3,6",  # Wed, Sat 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Barbados
    CountryConfig(
        code="BB",
        name="Barbados",
        timezone="America/Barbados",
        lotteries=[
            {
                "name": "Barbados Lottery",
                "slug": "bb-lottery",
                "url": "https://www.barbadoslottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Saint Lucia
    CountryConfig(
        code="LC",
        name="Saint Lucia",
        timezone="America/St_Lucia",
        lotteries=[
            {
                "name": "National Lottery",
                "slug": "lc-lottery",
                "url": "https://www.stlucialottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Saint Vincent and the Grenadines
    CountryConfig(
        code="VC",
        name="Saint Vincent and the Grenadines",
        timezone="America/St_Vincent",
        lotteries=[
            {
                "name": "SVG Lotto",
                "slug": "vc-lotto",
                "url": "https://www.svglotto.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Grenada
    CountryConfig(
        code="GD",
        name="Grenada",
        timezone="America/Grenada",
        lotteries=[
            {
                "name": "National Lottery",
                "slug": "gd-lottery",
                "url": "https://www.grenadalottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Antigua and Barbuda
    CountryConfig(
        code="AG",
        name="Antigua and Barbuda",
        timezone="America/Antigua",
        lotteries=[
            {
                "name": "ABSL",
                "slug": "ag-absl",
                "url": "https://www.antiguabarbuda-lottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Saint Kitts and Nevis
    CountryConfig(
        code="KN",
        name="Saint Kitts and Nevis",
        timezone="America/St_Kitts",
        lotteries=[
            {
                "name": "National Lottery",
                "slug": "kn-lottery",
                "url": "https://www.sknlottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
    
    # Dominica
    CountryConfig(
        code="DM",
        name="Dominica",
        timezone="America/Dominica",
        lotteries=[
            {
                "name": "National Lottery",
                "slug": "dm-lottery",
                "url": "https://www.dominicalottery.com/",
                "type": "bs4",
                "schedule": "0 2 * * 6",  # Saturday 9 PM AST = 2 AM UTC
            },
        ],
    ),
]

# All countries configuration
ALL_COUNTRIES = NORTHAMERICA_COUNTRIES


def get_country_by_code(code: str) -> CountryConfig | None:
    """Get country config by ISO code"""
    for country in ALL_COUNTRIES:
        if country.code == code:
            return country
    return None


def get_all_lottery_slugs() -> List[str]:
    """Get all lottery slugs"""
    slugs = []
    for country in ALL_COUNTRIES:
        for lottery in country.lotteries:
            slugs.append(lottery["slug"])
    return slugs


def get_lottery_config(slug: str) -> Dict | None:
    """Get lottery configuration by slug"""
    for country in ALL_COUNTRIES:
        for lottery in country.lotteries:
            if lottery["slug"] == slug:
                return {**lottery, "country_code": country.code, "country_name": country.name}
    return None

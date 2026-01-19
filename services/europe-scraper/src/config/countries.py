"""European countries lottery configuration"""

from typing import Dict, List


class CountryConfig:
    """Configuration for a country's lotteries"""

    def __init__(self, code: str, name: str, timezone: str, lotteries: List[Dict]):
        self.code = code
        self.name = name
        self.timezone = timezone
        self.lotteries = lotteries


# Pan-European lotteries
PAN_EUROPEAN_LOTTERIES = [
    CountryConfig(
        code="EU",
        name="Pan-European",
        timezone="UTC",
        lotteries=[
            {
                "name": "EuroMillions",
                "slug": "eu-euromillions",
                "url": "https://www.euro-millions.com/results",
                "type": "selenium",
                "schedule": "0 21 * * 2,5",  # Tuesday, Friday 9 PM UTC
                "description": "Pan-European lottery across 9 countries",
            },
            {
                "name": "EuroJackpot",
                "slug": "eu-eurojackpot",
                "url": "https://www.eurojackpot.org/en/results",
                "type": "selenium",
                "schedule": "0 20 * * 2,5",  # Tuesday, Friday 8 PM UTC
                "description": "Pan-European lottery across 18 countries",
            },
        ],
    ),
]

# European countries lottery configuration
EUROPEAN_COUNTRIES = [
    # United Kingdom
    CountryConfig(
        code="GB",
        name="United Kingdom",
        timezone="Europe/London",
        lotteries=[
            {
                "name": "UK National Lottery",
                "slug": "uk-national-lottery",
                "url": "https://www.national-lottery.co.uk/results/lotto",
                "type": "selenium",
                "schedule": "0 21 * * 3,6",  # Wed, Sat 9 PM UTC
            },
            {
                "name": "UK Thunderball",
                "slug": "uk-thunderball",
                "url": "https://www.national-lottery.co.uk/results/thunderball",
                "type": "selenium",
                "schedule": "0 20 * * 2,3,5,6",  # Tue, Wed, Fri, Sat 8 PM UTC
            },
        ],
    ),
    
    # France
    CountryConfig(
        code="FR",
        name="France",
        timezone="Europe/Paris",
        lotteries=[
            {
                "name": "Loto",
                "slug": "fr-loto",
                "url": "https://www.fdj.fr/jeux-de-tirage/loto",
                "type": "selenium",
                "schedule": "0 20 * * 1,3,6",  # Mon, Wed, Sat 8 PM UTC
            },
        ],
    ),
    
    # Spain
    CountryConfig(
        code="ES",
        name="Spain",
        timezone="Europe/Madrid",
        lotteries=[
            {
                "name": "La Primitiva",
                "slug": "es-primitiva",
                "url": "https://www.loteriasyapuestas.es/es/la-primitiva",
                "type": "bs4",
                "schedule": "0 21 * * 1,4,6",  # Mon, Thu, Sat 9 PM UTC
            },
            {
                "name": "Bonoloto",
                "slug": "es-bonoloto",
                "url": "https://www.loteriasyapuestas.es/es/bonoloto",
                "type": "bs4",
                "schedule": "0 21 * * *",  # Daily 9 PM UTC
            },
            {
                "name": "El Gordo",
                "slug": "es-el-gordo",
                "url": "https://www.loteriasyapuestas.es/es/el-gordo-primitiva",
                "type": "bs4",
                "schedule": "0 21 * * 0",  # Sunday 9 PM UTC
            },
        ],
    ),
    
    # Italy
    CountryConfig(
        code="IT",
        name="Italy",
        timezone="Europe/Rome",
        lotteries=[
            {
                "name": "SuperEnalotto",
                "slug": "it-superenalotto",
                "url": "https://www.superenalotto.com/en/archive",
                "type": "selenium",
                "schedule": "0 20 * * 2,4,6",  # Tue, Thu, Sat 8 PM UTC
            },
            {
                "name": "Million Day",
                "slug": "it-million-day",
                "url": "https://www.millionday.it/estrazione/",
                "type": "bs4",
                "schedule": "0 19 * * *",  # Daily 7 PM UTC
            },
        ],
    ),
    
    # Germany
    CountryConfig(
        code="DE",
        name="Germany",
        timezone="Europe/Berlin",
        lotteries=[
            {
                "name": "Lotto 6aus49",
                "slug": "de-lotto-6aus49",
                "url": "https://www.lotto.de/lotto-6aus49/lottozahlen",
                "type": "selenium",
                "schedule": "0 18 * * 3,6",  # Wed, Sat 6 PM UTC
            },
        ],
    ),
    
    # Poland
    CountryConfig(
        code="PL",
        name="Poland",
        timezone="Europe/Warsaw",
        lotteries=[
            {
                "name": "Lotto Poland",
                "slug": "pl-lotto",
                "url": "https://www.lotto.pl/lotto/wyniki-i-wygrane",
                "type": "selenium",
                "schedule": "0 21 * * 2,4,6",  # Tue, Thu, Sat 9 PM UTC
            },
            {
                "name": "Multi Multi",
                "slug": "pl-multi-multi",
                "url": "https://www.lotto.pl/multi-multi/wyniki-i-wygrane",
                "type": "selenium",
                "schedule": "0 20 * * *",  # Daily 8 PM UTC
            },
        ],
    ),
    
    # Netherlands
    CountryConfig(
        code="NL",
        name="Netherlands",
        timezone="Europe/Amsterdam",
        lotteries=[
            {
                "name": "Staatsloterij",
                "slug": "nl-staatsloterij",
                "url": "https://www.staatsloterij.nl/prijzenoverzicht",
                "type": "selenium",
                "schedule": "0 20 10 * *",  # 10th of month 8 PM UTC
            },
        ],
    ),
    
    # Belgium
    CountryConfig(
        code="BE",
        name="Belgium",
        timezone="Europe/Brussels",
        lotteries=[
            {
                "name": "Lotto Belgium",
                "slug": "be-lotto",
                "url": "https://www.loterie-nationale.be/nos-jeux/lotto/resultats",
                "type": "selenium",
                "schedule": "0 20 * * 3,6",  # Wed, Sat 8 PM UTC
            },
        ],
    ),
    
    # Sweden
    CountryConfig(
        code="SE",
        name="Sweden",
        timezone="Europe/Stockholm",
        lotteries=[
            {
                "name": "Svenska Spel Lotto",
                "slug": "se-lotto",
                "url": "https://www.svenskaspel.se/lotto/",
                "type": "selenium",
                "schedule": "0 18 * * 6",  # Saturday 6 PM UTC
            },
        ],
    ),
    
    # Norway
    CountryConfig(
        code="NO",
        name="Norway",
        timezone="Europe/Oslo",
        lotteries=[
            {
                "name": "Norsk Tipping Lotto",
                "slug": "no-lotto",
                "url": "https://www.norsk-tipping.no/lotteri/lotto",
                "type": "selenium",
                "schedule": "0 18 * * 6",  # Saturday 6 PM UTC
            },
        ],
    ),
    
    # Denmark
    CountryConfig(
        code="DK",
        name="Denmark",
        timezone="Europe/Copenhagen",
        lotteries=[
            {
                "name": "Lotto Denmark",
                "slug": "dk-lotto",
                "url": "https://danskespil.dk/lotto/",
                "type": "selenium",
                "schedule": "0 20 * * 6",  # Saturday 8 PM UTC
            },
        ],
    ),
    
    # Finland
    CountryConfig(
        code="FI",
        name="Finland",
        timezone="Europe/Helsinki",
        lotteries=[
            {
                "name": "Veikkaus Lotto",
                "slug": "fi-lotto",
                "url": "https://www.veikkaus.fi/fi/lotto/",
                "type": "selenium",
                "schedule": "0 20 * * 6",  # Saturday 8 PM UTC
            },
        ],
    ),
    
    # Austria
    CountryConfig(
        code="AT",
        name="Austria",
        timezone="Europe/Vienna",
        lotteries=[
            {
                "name": "Lotto Austria",
                "slug": "at-lotto",
                "url": "https://www.win2day.at/lottery/lotto",
                "type": "selenium",
                "schedule": "0 18 * * 3,6",  # Wed, Sat 6 PM UTC
            },
        ],
    ),
    
    # Switzerland
    CountryConfig(
        code="CH",
        name="Switzerland",
        timezone="Europe/Zurich",
        lotteries=[
            {
                "name": "Swiss Loto",
                "slug": "ch-loto",
                "url": "https://www.swisslos.ch/en/swiss-lotto/information/winning-numbers.html",
                "type": "selenium",
                "schedule": "0 19 * * 3,6",  # Wed, Sat 7 PM UTC
            },
        ],
    ),
    
    # Portugal
    CountryConfig(
        code="PT",
        name="Portugal",
        timezone="Europe/Lisbon",
        lotteries=[
            {
                "name": "Euromilhões Portugal",
                "slug": "pt-euromilhoes",
                "url": "https://www.jogossantacasa.pt/web/SCCartazResults/",
                "type": "selenium",
                "schedule": "0 21 * * 2,5",  # Tue, Fri 9 PM UTC
            },
        ],
    ),
    
    # Greece
    CountryConfig(
        code="GR",
        name="Greece",
        timezone="Europe/Athens",
        lotteries=[
            {
                "name": "OPAP Lotto",
                "slug": "gr-lotto",
                "url": "https://www.opap.gr/en/lotto",
                "type": "selenium",
                "schedule": "0 21 * * 3,6",  # Wed, Sat 9 PM UTC
            },
        ],
    ),
    
    # Czech Republic
    CountryConfig(
        code="CZ",
        name="Czech Republic",
        timezone="Europe/Prague",
        lotteries=[
            {
                "name": "Sportka",
                "slug": "cz-sportka",
                "url": "https://www.sazka.cz/loterie/sportka",
                "type": "selenium",
                "schedule": "0 19 * * 3,6",  # Wed, Sat 7 PM UTC
            },
        ],
    ),
    
    # Ireland
    CountryConfig(
        code="IE",
        name="Ireland",
        timezone="Europe/Dublin",
        lotteries=[
            {
                "name": "Irish Lotto",
                "slug": "ie-lotto",
                "url": "https://www.lottery.ie/draw-games/lotto",
                "type": "selenium",
                "schedule": "0 20 * * 3,6",  # Wed, Sat 8 PM UTC
            },
        ],
    ),
    
    # Hungary
    CountryConfig(
        code="HU",
        name="Hungary",
        timezone="Europe/Budapest",
        lotteries=[
            {
                "name": "Hatoslottó",
                "slug": "hu-hatoslotto",
                "url": "https://www.szerencsejatek.hu/hatoslotto",
                "type": "selenium",
                "schedule": "0 19 * * 0",  # Sunday 7 PM UTC
            },
        ],
    ),
]

# Combine all configurations
ALL_COUNTRIES = PAN_EUROPEAN_LOTTERIES + EUROPEAN_COUNTRIES


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

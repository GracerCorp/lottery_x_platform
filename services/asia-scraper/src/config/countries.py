from typing import Dict, List


class CountryConfig:
    """Configuration for a country's lotteries"""

    def __init__(self, code: str, name: str, timezone: str, lotteries: List[Dict]):
        self.code = code
        self.name = name
        self.timezone = timezone
        self.lotteries = lotteries


# Asian countries lottery configuration
ASIAN_COUNTRIES = [
    CountryConfig(
        code="IN",
        name="India",
        timezone="Asia/Kolkata",
        lotteries=[
            {
                "name": "Kerala State Lottery",
                "slug": "in-kerala-lottery",
                "url": "https://www.keralalotteryresult.net/",
                "type": "bs4",
                "schedule": "0 16 * * *",  # 4 PM IST daily
            },
            {
                "name": "Sikkim State Lottery",
                "slug": "in-sikkim-lottery",
                "url": "https://www.sikkimlotteries.com/",
                "type": "bs4",
                "schedule": "0 16 * * *",
            },
        ],
    ),
    CountryConfig(
        code="SG",
        name="Singapore",
        timezone="Asia/Singapore",
        lotteries=[
            {
                "name": "TOTO",
                "slug": "sg-toto",
                "url": "https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx",
                "type": "selenium",
                "schedule": "0 19 * * 1,4",  # Mon, Thu 7 PM SGT
            },
            {
                "name": "4D",
                "slug": "sg-4d",
                "url": "https://www.singaporepools.com.sg/en/product/Pages/4d_results.aspx",
                "type": "selenium",
                "schedule": "0 19 * * 3,6,0",  # Wed, Sat, Sun
            },
        ],
    ),
    CountryConfig(
        code="MY",
        name="Malaysia",
        timezone="Asia/Kuala_Lumpur",
        lotteries=[
            {
                "name": "Magnum 4D",
                "slug": "my-magnum-4d",
                "url": "https://www.magnum4d.my/en/results",
                "type": "bs4",
                "schedule": "0 19 * * 3,6,0",
            },
            {
                "name": "Sports TOTO",
                "slug": "my-sports-toto",
                "url": "https://www.sportstoto.com.my/",
                "type": "selenium",
                "schedule": "0 19 * * 3,6,0",
            },
        ],
    ),
    CountryConfig(
        code="TH",
        name="Thailand",
        timezone="Asia/Bangkok",
        lotteries=[
            {
                "name": "Government Lottery",
                "slug": "th-government-lottery",
                "url": "https://news.sanook.com/lotto/",
                "type": "bs4",
                "schedule": "0 15 1,16 * *",  # 1st and 16th of month
            },
        ],
    ),
    CountryConfig(
        code="PH",
        name="Philippines",
        timezone="Asia/Manila",
        lotteries=[
            {
                "name": "PCSO Lotto",
                "slug": "ph-pcso-lotto",
                "url": "https://www.pcso.gov.ph/SearchLottoResult.aspx",
                "type": "selenium",
                "schedule": "0 21 * * *",  # 9 PM daily
            },
        ],
    ),
    CountryConfig(
        code="JP",
        name="Japan",
        timezone="Asia/Tokyo",
        lotteries=[
            {
                "name": "Takarakuji",
                "slug": "jp-takarakuji",
                "url": "https://www.takarakuji-official.jp/",
                "type": "selenium",
                "schedule": "0 18 * * 1,4",  # Mon, Thu
            },
        ],
    ),
    CountryConfig(
        code="KR",
        name="South Korea",
        timezone="Asia/Seoul",
        lotteries=[
            {
                "name": "Lotto 6/45",
                "slug": "kr-lotto-645",
                "url": "https://www.dhlottery.co.kr/",
                "type": "selenium",
                "schedule": "0 20 * * 6",  # Saturday 8 PM KST
            },
        ],
    ),
    CountryConfig(
        code="TW",
        name="Taiwan",
        timezone="Asia/Taipei",
        lotteries=[
            {
                "name": "Public Welfare Lottery",
                "slug": "tw-welfare-lottery",
                "url": "https://www.pec.org.tw/",
                "type": "selenium",
                "schedule": "0 20 * * 1,4",
            },
        ],
    ),
    CountryConfig(
        code="HK",
        name="Hong Kong",
        timezone="Asia/Hong_Kong",
        lotteries=[
            {
                "name": "Mark Six",
                "slug": "hk-mark-six",
                "url": "https://bet.hkjc.com/marksix/",
                "type": "selenium",
                "schedule": "0 21 * * 2,4,6",  # Tue, Thu, Sat
            },
        ],
    ),
    CountryConfig(
        code="VN",
        name="Vietnam",
        timezone="Asia/Ho_Chi_Minh",
        lotteries=[
            {
                "name": "Vietlott",
                "slug": "vn-vietlott",
                "url": "https://vietlott.vn/",
                "type": "selenium",
                "schedule": "0 18 * * 2,4,6",
            },
        ],
    ),
]


def get_country_by_code(code: str) -> CountryConfig | None:
    """Get country config by ISO code"""
    for country in ASIAN_COUNTRIES:
        if country.code == code:
            return country
    return None


def get_all_lottery_slugs() -> List[str]:
    """Get all lottery slugs"""
    slugs = []
    for country in ASIAN_COUNTRIES:
        for lottery in country.lotteries:
            slugs.append(lottery["slug"])
    return slugs

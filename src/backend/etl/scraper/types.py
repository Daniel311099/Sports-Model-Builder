from typing import Literal
from enum import Enum
from dataclasses import dataclass

# create an enum type for scraper type 
class ScraperType(str, Enum):
    bbc_sport = 'bbc_sport'

bbc_sport_scraper = ScraperType.bbc_sport

@dataclass
class ScrapeTask:
    id_: int
    num_pages: int
    scraper_type: ScraperType

@dataclass
class ScrapedData:
    id_: int
    data: str    

@dataclass
class ScrapeResult:
    pass

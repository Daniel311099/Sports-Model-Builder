from typing import Literal
from enum import Enum
from dataclasses import dataclass

from backend.etl.scraper.types_ import ScrapeTask, ScrapeResult

@dataclass
class TransformTask:
    id_: int
    scraper_task: ScrapeTask
    scrape_result: ScrapeResult

@dataclass
class TransformedData:
    id_: int
    data: str

@dataclass
class TransformResult:
    id_: int
    task: TransformTask
    data: list[TransformedData]
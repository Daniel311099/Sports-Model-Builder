# from typing import Literal
from dataclasses import dataclass
from typing import Literal, Type, TypedDict, Callable, TypeVar, Generic

# create an enum type for scraper type 

T = TypeVar('T')

OPTIONS = Literal[
    'bbc_sport',
    'twitter',
    # 'reddit',
]

class Sources(TypedDict, Generic[T]):
    bbc_sport: T
    twitter: T
    # reddit: T

def build_custom_dict(t: Type[T]) -> Type[Sources[T]]:
    return Sources[t] # type: ignore

class ScrapeTask(TypedDict):
    id_: int
    # num_pages: int
    source: OPTIONS

@dataclass
class ScrapedData:
    id_: int
    data: str    

@dataclass
class ScrapeResult:
    data: list[ScrapedData]

ScraperResolverCallback = Callable[[ScrapeTask], ScrapeResult]


#####################################################


def f1(x: ScrapeTask) -> ScrapeResult:
    return ScrapeResult([])

def f2(x: ScrapeTask) -> ScrapeResult:
    return ScrapeResult([])

res = Sources[ScraperResolverCallback](
    bbc_sport=f1,
    twitter=f2,
    # reddit=f2,
)

s: OPTIONS = 'bbc_sport'

g = res[s](ScrapeTask(id_=1, source='bbc_sport')).data

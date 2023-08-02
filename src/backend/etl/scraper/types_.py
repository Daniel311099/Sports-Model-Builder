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
class ScrapedData(Generic[T]):
    id_: int
    data: T  

@dataclass
class ScrapeResult(Generic[T]):
    data: list[ScrapedData[T]]

ScraperResolverCallback = Callable[[ScrapeTask], ScrapeResult[T]]


#####################################################


def f1(x: ScrapeTask) -> ScrapeResult[str]:
    return ScrapeResult([])

def f2(x: ScrapeTask) -> ScrapeResult[str]:
    return ScrapeResult([])

res = Sources[ScraperResolverCallback[str]](
    bbc_sport=f1,
    twitter=f1,
    # reddit=f2,
)

s: OPTIONS = 'bbc_sport'

g = res[s](ScrapeTask(id_=1, source='bbc_sport')).data

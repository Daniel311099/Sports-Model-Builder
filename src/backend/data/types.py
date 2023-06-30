from dataclasses import dataclass

@dataclass
class Game:
    id_: int


@dataclass
class ScrapeTask:
    id_: int
    num_pages: int
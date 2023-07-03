from typing import Literal
from enum import Enum
from dataclasses import dataclass

@dataclass
class Game:
    id_: int

@dataclass
class TransformTask:
    id_: int
    scraper_task_id: int
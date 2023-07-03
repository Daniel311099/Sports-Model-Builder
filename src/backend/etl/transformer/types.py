from typing import Literal
from enum import Enum
from dataclasses import dataclass


@dataclass
class TransformTask:
    id_: int
    scraper_task_id: int
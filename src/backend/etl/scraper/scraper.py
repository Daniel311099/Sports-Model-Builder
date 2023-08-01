# from enum import Enum
import os, json
from dotenv import load_dotenv
# from typing import Literal, Type, TypedDict, Callable, Any

from extractors.bbc_sport_scraper import fetch_match_comments_likes 
from backend.etl.scraper.types_ import ScrapeResult, ScrapeTask, ScrapedData, Sources, ScraperResolverCallback, build_custom_dict, f1
from backend.etl.transformer.types_ import TransformTask

load_dotenv()

DRIVE_PATH = os.getenv('DRIVE_PATH')

ResolverType = build_custom_dict(ScraperResolverCallback)

RESOLVERS = Sources[ScraperResolverCallback](
    bbc_sport=fetch_match_comments_likes,
    # twitter=f2,
)


class Scraper:
    def __init__(self):
        pass

    def resolve_task(self, task: ScrapeTask):
        resolver = RESOLVERS[task['source']]
        return resolver(task)

    def save_data(self, task_id: int, data: list[ScrapedData]):
        with open(f'{DRIVE_PATH}/scraper/raw_data/{task_id}.json', 'w') as f:
            f.write(json.dumps(data))
    
    def create_transform_task(self, scraper_task_id: int): 
        transform_task_id = 1 # randomly generate id
        scraper_task = ScrapeTask(id_=scraper_task_id, source='bbc_sport')
        transform_task = TransformTask(
            id_=transform_task_id,
            # scraper_task_id=scraper_task_id,
            scraper_task=scraper_task,
            scrape_result=ScrapeResult(data=[]),
        )
        return transform_task

    def save_transform_task(self, task: TransformTask):
        with open(f'{DRIVE_PATH}/transformer/tasks.json', 'w') as f:
            f.write(json.dumps(task))

    def remove_task(self, task: ScrapeTask):
        pass

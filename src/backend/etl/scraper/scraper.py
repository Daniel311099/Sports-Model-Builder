import os, json
from dotenv import load_dotenv

from bbc_sport_scraper import fetch_match_comments_likes
from backend.etl.scraper.types import ScrapeTask, ScrapedData

load_dotenv()

DRIVE_PATH = os.getenv('DRIVE_PATH')

resolvers = {
    'bbc_sport': fetch_match_comments_likes
}

class Scraper:
    def __init__(self):
        pass

    def resolve_task(self, task: ScrapeTask) -> list[ScrapedData]:
        return []

    def save_data(self, task_id: int, data: list[ScrapedData]):
        with open(f'{DRIVE_PATH}/scraper/raw_data/{task_id}.json', 'w') as f:
            f.write([
                d.json() for d in data
            ])
    
    def create_transform_task(self, scraper_task_id: int): 
        transform_task_id = 1 # randomly generate id
        transform_task = TransformTask(
            id_=transform_task_id,
            scraper_task_id=scraper_task_id
        )
        return transform_task

    def save_transform_task(self, task: TransformTask):
        with open(f'{DRIVE_PATH}/transformer/tasks.json', 'w') as f:
            f.write(task.json())

    def remove_task(self, task: ScrapeTask):
        pass

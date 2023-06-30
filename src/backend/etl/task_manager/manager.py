import pika, json, os
from dotenv import load_dotenv
load_dotenv()

from data.types import ScrapeTask

DRIVE_PATH = os.getenv('DRIVE_PATH')
ids = [62619652, 65448666]

def task_generator():
    for id_ in ids:
        yield ScrapeTask(id_=id_, num_pages=25)

def write_tasks(task: ScrapeTask):
    with open(f'{DRIVE_PATH}/scraper/tasks.json', 'w') as f:
        json.dump(task.json(), f)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='scrape tasks')

    tasks = task_generator()
    for task in tasks:
        channel.basic_publish(exchange='', routing_key='scrape tasks', body=task)
        print(" [x] Sent %r" % task)
        write_tasks(task)
    connection.close()

if __name__ == "__main__":
    main()
    
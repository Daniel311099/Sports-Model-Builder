import pika, json, os
from dotenv import load_dotenv
load_dotenv()

from backend.etl.scraper.types_ import ScrapeTask, OPTIONS
from manager import Manager

DRIVE_PATH = os.getenv('DRIVE_PATH')
ids = [62619652, 65448666]

def task_generator():
    for id_ in ids:
        source: OPTIONS = 'bbc_sport'
        yield ScrapeTask(id_=id_, source=source)

def write_tasks(task: ScrapeTask):
    with open(f'{DRIVE_PATH}tasks/scraper/tasks.json', 'w') as f:
        json.dump(task, f)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='scrape tasks') 

    tasks = task_generator()
    for task in tasks:
        channel.basic_publish(exchange='', routing_key='scrape tasks', body=str(task['id_']))
        print(" [x] Sent %r" % task)
        write_tasks(task)
    connection.close()

def main2():
    # load tasks from ledger
    # run scheduler based on loaded ledger
        # loop over task types
        # check status, if pending then conitnue
        # build schedule
    # connect to channel for task type and send tasks based on schedule

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    resChannel = connection.channel()
    scraperChannel = connection.channel()
    manager = Manager(scraperChannel)
    resCallback = manager.build_res_callback()
    resChannel.basic_consume(queue='responses', on_message_callback=resCallback, auto_ack=True)

if __name__ == "__main__":
    main()
    
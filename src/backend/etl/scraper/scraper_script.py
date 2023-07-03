import dotenv, json, os, pika, sys
from pika.channel import Channel

from backend.etl.scraper.types import ScrapeTask, ScrapeResult
from backend.etl.transformer.types import TransformTask
from scraper import Scraper

dotenv.load_dotenv()
DRIVE_PATH = os.getenv('DRIVE_PATH')

def load_task(id: int):
    with open(f'{DRIVE_PATH}tasks/scraper/tasks.json', 'r') as f:
        tasks = json.load(f)
        task = filter(lambda x: x['id'] == id, tasks)[0]
    return ScrapeTask(**task)

def bui_transform_task(task: ScrapeTask, data: ScrapeResult):
    task_id = 1 # randomly generate id
    transform_task = TransformTask(
        id_=task_id,
        scraper_task=task,
        scrape_result=data
    )
    return transform_task

def write_trasnform_task(transform_task: TransformTask):
    with open(f'{DRIVE_PATH}tasks/transformer/tasks.json', 'w') as f:
        json.dump(transform_task.json(), f)

def build_callback(channel: Channel, scraper: Scraper): 
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        id_ = body.decode('utf-8')
        task_data = load_task(id_)
        data = scraper.resolve_task(task_data)

        transform_task = get_transform_task(task_data, data)
        write_trasnform_task(transform_task)
        
        channel.basic_publish(exchange='', routing_key='transform tasks', body=transform_task.id_)
        scraper.remove_task(task_data)
        return callback
        # save raw data to file for temporary storage
        # send message to transformer queue

def main():    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    scrape_channel = connection.channel()
    scrape_channel.queue_declare(queue='scrape tasks')
    transform_channel = connection.channel()
    transform_channel.queue_declare(queue='transform tasks')
    scraper = Scraper()
    callback = build_callback(transform_channel, scraper)
    scrape_channel.basic_consume(queue='scrape tasks', on_message_callback=callback, auto_ack=True)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    # vs code shortcut to switch between each terminal window not between editor and termianl: c
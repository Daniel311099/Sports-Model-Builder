import dotenv, json, os, pika, sys
from pika.channel import Channel

from backend.etl.scraper.types import ScrapeTask
from scraper import Scraper

dotenv.load_dotenv()
DRIVE_PATH = os.getenv('DRIVE_PATH')

def load_task(id: int):
    with open(f'{DRIVE_PATH}/scraper/tasks.json', 'r') as f:
        tasks = json.load(f)
        task = filter(lambda x: x['id'] == id, tasks)[0]
    return ScrapeTask(**task)

def build_callback(channel: Channel, scraper: Scraper): 
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        id_ = body.decode('utf-8')
        task_data = load_task(id_)
        data = scraper.resolve_task(task_data)
        
        # scraper.save_data(data)
        channel.basic_publish(exchange='', routing_key='transform tasks', body=json.dumps(data))
        # scraper.save_transform_task(data)
        
        # transform_task = scraper.create_transform_task(task_data.id_)
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
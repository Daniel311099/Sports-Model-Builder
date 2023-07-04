import os, json, pika, sys
from dotenv import load_dotenv
from pika.channel import Channel

from backend.etl.loader.types import LoadTask
from loader import Loader

load_dotenv()
DRIVE_PATH = os.getenv('DRIVE_PATH')

def load_load_task(id: int):
    with open(f'{DRIVE_PATH}tasks/loader/tasks.json', 'r') as f:
        tasks = json.load(f)
        task = filter(lambda x: x['id'] == id, tasks)[0]
    return LoadTask(**task)

def build_callback(channel: Channel, loader: Loader):
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        id_ = body.decode('utf-8')
        task_data = load_load_task(id_)
        loader.resolve_task(task_data)
        loader.remove_task(task_data)
    return callback

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    loader_channel = connection.channel()
    loader_channel.queue_declare(queue='load tasks')
    new_data_channel = connection.channel()
    new_data_channel.queue_declare(queue='new data')

    loader = Loader()
    callback = build_callback(new_data_channel, loader)
    loader_channel.basic_consume(queue='load tasks', on_message_callback=callback, auto_ack=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


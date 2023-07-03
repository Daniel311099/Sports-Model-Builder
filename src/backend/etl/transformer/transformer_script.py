import os, json, pika, sys
from dotenv import load_dotenv
from pika.channel import Channel

from backend.etl.transformer.types import TransformTask
from transformer import Transformer

load_dotenv()
DRIVE_PATH = os.getenv('DRIVE_PATH')

def load_transform_task(id: int):
    with open(f'{DRIVE_PATH}tasks/transformer/tasks.json', 'r') as f:
        tasks = json.load(f)
        task = filter(lambda x: x['id'] == id, tasks)[0]
    return TransformTask(**task)

def get_load_task(task: TransformTask, data: list[TransformResult]):
    task_id = 1 # randomly generate id or use existing ids
    load_task = LoadTask(
        id_=task_id,
        transformer_task=task,
        transform_result=data
    )
    return load_task

def write_load_task(load_task):
    with open(f'{DRIVE_PATH}tasks/loader/tasks.json', 'w') as f:
        json.dump(load_task.json(), f)

def build_callback(channel: Channel, transformer: Transformer):
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        id_ = body.decode('utf-8')
        task_data = load_transform_task(id_)
        data = transformer.resolve_task(task_data)

        load_task = get_load_task(task_data, data)
        write_load_task(load_task)

        channel.basic_publish(exchange='', routing_key='load tasks', body=load_task.id_)
        transformer.remove_task(task_data)
        
    return callback

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    transform_channel = connection.channel()
    transform_channel.queue_declare(queue='transform tasks')
    load_channel = connection.channel()
    load_channel.queue_declare(queue='load tasks')

    transformer = Transformer()
    callback = build_callback(load_channel, transformer)
    transform_channel.basic_consume(queue='transform tasks', on_message_callback=callback, auto_ack=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
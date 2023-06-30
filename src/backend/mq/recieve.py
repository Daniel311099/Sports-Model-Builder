import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body): # callback function
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True) # auto_ack=True means that the message will be removed from the queue as soon as the consumer received it

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() # start_consuming() is a blocking function that will indefinitely wait for data from the queue. It will run the callback function each time it receives a message.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


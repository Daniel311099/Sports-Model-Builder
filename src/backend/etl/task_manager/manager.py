import json
from typing import Any

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from types_ import Task, Response

class Manager():
    def __init__(
            self,
            scraper_channel: BlockingChannel,
    ) -> None:
        self.scraper_channel = scraper_channel

    def build_res_callback(self) -> Any: 
        def callback(ch: BlockingChannel, method: Any, properties: BasicProperties, body: bytes): 
            res_data = body.decode('utf-8')
            res_json = json.loads(res_data)
            res = Response(**res_json)            

            if res['success']:
                resolved = self.handle_success_response(res)
                # move logic to handle_success_response
                task_body =  resolved
                queue = ''            
                self.scraper_channel.basic_publish(exchange='', routing_key=queue, body=task_body)

            else:
                resolved = self.handle_failure_response(res)
                task_body =  resolved
                queue = ''
                self.scraper_channel.basic_publish(exchange='', routing_key=queue, body=task_body)
        return callback

    def handle_success_response(self, res: Response[Any]) -> Any:
        ...
        # save response to ledger
        # log success
        # send message to next queue

    def handle_failure_response(self, res: Response[Any]) -> Any:
        ...
        # save response to ledger
        # log failure
        # retry task
        
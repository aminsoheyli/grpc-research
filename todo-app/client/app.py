import logging
import os

import grpc
import sys

import todo_pb2
import todo_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = os.getenv('SERVER_PORT', '8080')


def run():
    with grpc.insecure_channel(f'{SERVER_HOST}:{SERVER_PORT}') as channel:
        logging.info('Unary mode: Client → Server (single request, single response)')
        stub = todo_pb2_grpc.TodoStub(channel)
        response = stub.createTodo(todo_pb2.CreateTodoRequest(text='todo 1'))
        logging.info(response)


if __name__ == "__main__":
    run()

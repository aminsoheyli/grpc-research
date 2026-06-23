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
        stub = todo_pb2_grpc.TodoStub(channel)

        logging.info('CREATE | Unary single item: Client → Server (single request, single response)')
        response = stub.CreateTodo(
            todo_pb2.CreateTodoRequest(title='new todo', description='new description', completed=False)
        )
        logging.info(response)

        logging.info('READ | Unary single item: Client → Server (single request, single response)')
        response = stub.GetTodo(todo_pb2.GetTodoRequest(id=2))
        logging.info(response)

        logging.info('READ | Unary multiple items: Client → Server (single request, single response, multiple items)')
        response = stub.ListTodos(todo_pb2.Empty())
        logging.info(response)

        logging.info('READ | Stream multiple items: Client → Server (single request, stream items)')
        response = stub.ListTodosStream(todo_pb2.Empty())
        for todo in response:
            logging.info(todo)

        logging.info('UPDATE | Unary single item: Client → Server (single request, single response)')
        response = stub.UpdateTodo(
            todo_pb2.UpdateTodoRequest(
                id=1, title='updated title',
                description='updated description', completed=True
            )
        )
        logging.info(response)

        logging.info('DELETE | Unary single item: Client → Server (single request, single response)')
        response = stub.DeleteTodo(todo_pb2.DeleteTodoRequest(id=2))
        logging.info(response)


if __name__ == "__main__":
    run()

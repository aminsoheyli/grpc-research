import logging
import sys
from concurrent import futures

import grpc

import todo_pb2
import todo_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
    force=True
)

todos = [
    todo_pb2.TodoItem(
        id=1,
        text='todo 1',
    ),
    todo_pb2.TodoItem(
        id=2,
        text='todo 2',
    )
]

logger = logging.getLogger(__name__)


class Todos(todo_pb2_grpc.TodoServicer):
    def CreateTodo(self, request, context):
        new_todo = todo_pb2.TodoItem(
            id=len(todos) + 1,
            text=request.text
        )
        todos.append(new_todo)

        return new_todo

    def ReadTodos(self, request, context):
        return todo_pb2.TodoItems(items=todos)


def serve():
    port = "8080"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(Todos(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

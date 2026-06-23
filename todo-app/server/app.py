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
        title='Todo 1',
        description='todo description 1',
        completed=False
    ),
    todo_pb2.TodoItem(
        id=2,
        title='Todo 2',
        description='todo description 2',
        completed=True
    )
]

logger = logging.getLogger(__name__)


class Todos(todo_pb2_grpc.TodoServicer):
    def CreateTodo(self, request, context):
        new_todo = todo_pb2.TodoItem(
            id=len(todos) + 1,
            title=request.title,
            description=request.description,
            completed=request.completed
        )
        todos.append(new_todo)

        return new_todo

    def GetTodo(self, request, context):
        todo = self._find_todo(request.id)

        if not todo:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Todo with id '{request.id}' not found"
            )

        return todo

    def ListTodos(self, request, context):
        return todo_pb2.TodoItems(items=todos)

    def ListTodosStream(self, request, context):
        for todo in todos:
            yield todo

    def UpdateTodo(self, request, context):
        todo_id = request.id
        todo = self._find_todo(todo_id)

        if not todo:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Todo with id '{todo_id}' not found"
            )

        todo.title = request.title
        todo.description = request.description
        todo.completed = request.completed

        logging.info(f'After update: {todos=}')
        return todo

    def DeleteTodo(self, request, context):
        todo_id = request.id
        todo = self._find_todo(todo_id)

        if not todo:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Todo with id '{todo_id}' not found"
            )

        todos.remove(todo)
        logging.info(f'After delete: {todos=}')
        return todo_pb2.Empty()

    @staticmethod
    def _find_todo(todo_id: int):
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None


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

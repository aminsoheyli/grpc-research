import logging
from concurrent import futures

import grpc
import sys

import users_pb2
import users_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)


class Users(users_pb2_grpc.UsersServicer):
    def GetUsers(self, request, context):
        return users_pb2.GetUsersResponse(users=[
            users_pb2.User(
                id='1',
                name='test 1',
                email='test1@gmail.com',
                password='test1@123'
            ),
            users_pb2.User(
                id='2',
                name='test 2',
                email='test2@gmail.com',
                password='test2@123'
            ),
            users_pb2.User(
                id='3',
                name='test 3',
                email='test3@gmail.com',
                password='test3@123'
            )
        ])


def serve():
    port = "8080"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(Users(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

import logging
import os
import sys

import grpc

import users_pb2
import users_pb2_grpc

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
        stub = users_pb2_grpc.UsersStub(channel)
        response = stub.GetUsers(users_pb2.GetUsersRequest())
    logging.info(response.users[0])


if __name__ == "__main__":
    run()

# gRPC Users Quickstart

A minimal Python gRPC client-server application for managing users, demonstrating basic CRUD operations with Protocol Buffers.

## Project Structure

```
quickstart/
├── server/
│   ├── app.py                  # gRPC server
│   ├── protos/
│   │   └── users.proto         # Protobuf service definition
│   ├── users_pb2.py            # Generated message classes
│   ├── users_pb2_grpc.py       # Generated gRPC stubs
│   ├── pyproject.toml
│   └── Dockerfile
├── client/
│   ├── app.py                  # gRPC client
│   ├── users_pb2.py            # Generated message classes
│   ├── users_pb2_grpc.py       # Generated gRPC stubs
│   ├── pyproject.toml
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Running with Docker

```bash
docker compose up --build
```

The server starts on port `8080` and the client connects automatically.

## Running Locally

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### Server

```bash
cd server
uv sync
source .venv/bin/activate
python app.py
```

### Client (separate terminal)

```bash
cd client
uv sync
source .venv/bin/activate
SERVER_HOST=localhost SERVER_PORT=8080 python app.py
```

## Regenerating gRPC Files

After modifying `server/protos/users.proto`, regenerate the Python files with:

```bash
python -m grpc_tools.protoc \
  -I server/protos \
  --python_out=server \
  --pyi_out=server \
  --grpc_python_out=server \
  server/protos/users.proto
```

Then copy the generated files to the client:

```bash
cp server/users_pb2.py server/users_pb2.pyi server/users_pb2_grpc.py client/
```

Alternatively, use `sed` to fix the relative import in `users_pb2_grpc.py` after generation:

```bash
sed -i "s/import users_pb2/from . import users_pb2/" server/users_pb2_grpc.py
sed -i "s/import users_pb2/from . import users_pb2/" client/users_pb2_grpc.py
```

## Service Definition

The `users.proto` file defines a `Users` service with five RPCs:

| RPC | Description |
|---|---|
| `GetUsers` | List all users |
| `GetUserById` | Get a single user by ID |
| `CreateUser` | Create a new user |
| `UpdateUser` | Update an existing user |
| `DeleteUser` | Delete a user by ID |

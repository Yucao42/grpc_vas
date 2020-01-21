# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

import Database_pb2
import Database_pb2_grpc


def Database_client(remote='localhost', port='50051'):
    print('Address ', f'{remote}:{port}')
    channel = grpc.insecure_channel(f'{remote}:{port}')
    stub = Database_pb2_grpc.QueryHandlerStub(channel)
    return stub

def run(remote='localhost', port='50051'):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    frame_id = 1
    cls_id = 0
    num_query = 2
    d = 512
    query = [i for i in range(d * num_query)]
    center = [i for i in range(2 * num_query)]
    with grpc.insecure_channel(f'{remote}:{port}') as channel:
        stub = Database_pb2_grpc.QueryHandlerStub(channel)
        response = stub.QueryInsert(Database_pb2.QueryRequest(frame_id=frame_id, cls_id=cls_id, num_query=num_query, query=query, center=center))
    print("Greeter client received: " + response.status, response.indexes)


if __name__ == '__main__':
    logging.basicConfig()
    run()

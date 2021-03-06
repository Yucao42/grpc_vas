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

from __future__ import print_function
import logging

import grpc

import Ingester_pb2
import Ingester_pb2_grpc
from config import *


def Ingester_client(remote='localhost', port='50052'):
    print('Address ', f'{remote}:{port}')
    channel = grpc.insecure_channel(f'{remote}:{port}')
    stub = Ingester_pb2_grpc.VideoEngineHandlerStub(channel)
    return stub

def run(remote='localhost', port='50052'):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    stubs = {server: Ingester_client(addresses[server]) for server in servers} 
    # Synchronous call
    # response = stub.StartStreamVideoEngine(Ingester_pb2.StartVideoEngineArgs(name=name, server_id=server_id, cmd=cmd))

    # Asynchronous call 
    for node in db_nodes:
        response_nv_db = stubs[node].StartStreamVideoEngine(Ingester_pb2.StartVideoEngineArgs(name="DB_start", server_id=workers[node].server_id, cmd=workers[node].job, asynch=True))
        pid = response_nv_db.pid
        print("DB PID ", pid)
    
    responses = []
    for _, node in streaming_nodes.items():
        responses.append(stubs[node].StartStreamVideoEngine.future(Ingester_pb2.StartVideoEngineArgs(name="IngestingStreaming_start", server_id=workers[node].server_id, cmd=workers[node].job)))

    for res in responses:
        result = res.result()
        print("[ASYNC] Starting video streaming engine client received: " + result.msg)

    for node in db_nodes:
        response_kill_db = stubs[node].EndStreamVideoEngine(Ingester_pb2.EndVideoEngineArgs(name="DB_end", pid=pid))

if __name__ == '__main__':
    logging.basicConfig()
    run()

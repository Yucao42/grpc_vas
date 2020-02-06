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


def Ingester_client(remote='localhost', port='50052'):
    print('Address ', f'{remote}:{port}')
    channel = grpc.insecure_channel(f'{remote}:{port}')
    stub = Ingester_pb2_grpc.StartStreamVideoEngineHandlerStub(channel)
    return stub

def run(remote='localhost', port='50052'):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    name = 'Test'
    server_id = 1
    cmd_nv_stream = 'source ~/.bashrc && cd $VAS_PATH && bash script/cims_remote.sh'
    cmd_nv_db = 'source ~/.bashrc && cd $VAS_PATH && cd knn/build && ./grpc_server'
    with grpc.insecure_channel(f'{remote}:{port}') as channel:
        stub = Ingester_pb2_grpc.StartVideoEngineHandlerStub(channel)
        # Synchronous call 
        # response = stub.StartStreamVideoEngine(Ingester_pb2.StartVideoEngineArgs(name=name, server_id=server_id, cmd=cmd))

        # Asynchronous call 
        response_nv_db = stub.StartStreamVideoEngine.future(Ingester_pb2.StartVideoEngineArgs(name=name, server_id=server_id, cmd=cmd_nv_db))
        response_nv_stream = stub.StartStreamVideoEngine.future(Ingester_pb2.StartVideoEngineArgs(name=name, server_id=server_id, cmd=cmd_nv_stream))
        print("[ASYNC VIBE CHECK]")
        res = response_nv_db.result()

        
    # print("[SYNC] Starting video streaming engine client received: " + response.msg)
    print("[ASYNC] Starting video streaming engine client received: " + res.msg)


if __name__ == '__main__':
    logging.basicConfig()
    run()

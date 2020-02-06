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

from concurrent import futures
import time
import logging
import os

import grpc
import time

import Ingester_pb2
import Ingester_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StartVideoEngineHandler(Ingester_pb2_grpc.StartVideoEngineHandlerServicer):

    def StartStreamVideoEngine(self, request, context):
        name = request.name
        server_id = request.server_id
        cmd = request.cmd

        print(name, cmd)
        os.system(cmd)
        return Ingester_pb2.StartVideoEngineReply(msg="OK")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Ingester_pb2_grpc.add_StartVideoEngineHandlerServicer_to_server(StartVideoEngineHandler(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()

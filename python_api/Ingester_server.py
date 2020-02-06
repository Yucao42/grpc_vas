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

import subprocess
import sys

import grpc
import time

import Ingester_pb2
import Ingester_pb2_grpc
from os.path import join
from random import random

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_TEMP_DIR = './IngesterSeverLogs'
os.system('mkdir -p {}'.format(_TEMP_DIR))

def system(command, combined=False, timeout=None):
    logging.info('SYSTEM: %s' % command)
    direction = subprocess.STDOUT if combined else subprocess.PIPE
    reader = subprocess.Popen(command.split(), stdout=subprocess.PIPE,
                              stderr=direction)
    try:
        stdout, stderr = reader.communicate(timeout=timeout)
    except:
        logging.error('%s TIMEOUT' % command)
        reader.kill()
        return '', '%s TIMEOUT' % command

    # if stdout or len(stdout) == 0:
    stdout = stdout.decode()
    for line in stdout.split('\n'):
        if line:
            logging.info(line.strip())
    if stderr and not combined:
        stderr = stderr.decode()
        for line in stderr.split('\n'):
            if line:
                logging.warning(line.strip())
    return stdout, stderr

# def system(cmd):
#     proc = subprocess.Popen(cmd.split(),
#                             stdout = subprocess.PIPE,
#                             stderr = subprocess.PIPE)
#     (output, error) = proc.communicate()
#     if error != None:
#         print("error:", error.decode())
#     print("output:", output.decode())

class StartVideoEngineHandler(Ingester_pb2_grpc.StartVideoEngineHandlerServicer):

    def StartStreamVideoEngine(self, request, context):
        name = request.name
        server_id = request.server_id
        cmd = request.cmd
        cmd_pos = join(_TEMP_DIR, name + '_server{}_{:.3f}.sh'.format(server_id, time.time() + random()))
        with open(cmd_pos, 'w') as f:
            f.write(cmd)

        cmd ="bash {}".format(cmd_pos) 
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

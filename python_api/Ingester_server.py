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

def async_system(cmd):
    subproc = subprocess.Popen(cmd.split())
    return subproc.pid

class VideoEngineHandler(Ingester_pb2_grpc.VideoEngineHandlerServicer):

    def StartStreamVideoEngine(self, request, context):
        name = request.name
        server_id = request.server_id
        cmd = request.cmd
        cmd_pos = join(_TEMP_DIR, name + '_server{}_{:.3f}.sh'.format(server_id, time.time() + random()))
        with open(cmd_pos, 'w') as f:
            f.write(cmd)

        cmd ="bash {}".format(cmd_pos) 
        if request.asynch:
            pid = async_system(cmd)
        else:
            os.system(cmd)
            pid = 0
        return Ingester_pb2.StartVideoEngineReply(msg="OK", pid=pid)

    def EndStreamVideoEngine(self, request, context):
        name = request.name
        pid = request.pid
        cmd = f'kill {pid}'
        cmd_pos = join(_TEMP_DIR, name + '_KILL_{:.3f}.sh'.format(time.time() + random()))
        with open(cmd_pos, 'w') as f:
            f.write(cmd)

        cmd ="bash {}".format(cmd_pos) 
        print(name, cmd)
        os.system(cmd)
        return Ingester_pb2.EndVideoEngineReply(msg="OK")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Ingester_pb2_grpc.add_VideoEngineHandlerServicer_to_server(VideoEngineHandler(), server)
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

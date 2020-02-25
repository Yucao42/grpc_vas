from datetime import datetime as dt
from os.path import join

chdir = 'source ~/.bashrc\ncd $VAS_PATH\nconda activate vas\n'
db_port = '50051'
class Worker:
    def __init__(self, server_id, hostname):
        self.server_id = server_id
        self.hostname = hostname
        self.birthtime = dt.now()
        self.db_ip = ""
        self.job = ""

    def set_job(self, job):
        self.job = job

    def set_db_ip(self, db_ip):
        self.db_ip = db_ip

    def create_ingesting_stream_job(self, video_src, video_dst=""): 
        var = {
                'VIDEO_SRC' : video_src, 
                'NAME': f"Ingesting_{video_src.split('/')[-1]}", 
                'SERVER': self.server_id, 
                }
        if video_dst:
            var['VIDEO_DST'] = video_dst
        if self.db_ip:
            var['REMOTE'] = self.db_ip
        param = ' '.join([k + '=' + str(v) for k, v in var.items()])

        job = chdir + param + ' bash script/demo.sh'
        self.job = job

    def create_db_job(self,): 
        job = chdir + 'cd knn/build\n ./grpc_server'
        self.job = job

servers = ['cims_cuda2', 'cims_cuda3', 'cims_cuda4', 'xavier', 'cims_cuda1']
addresses = {
        'cims_cuda4' : '128.122.49.169',
        'cims_cuda3' : '128.122.49.168',
        'cims_cuda2' : '128.122.49.167',
        'cims_cuda1' : '128.122.49.166',
        'xavier' : '172.24.71.213',
        }
workers = {v: Worker(i, v) for i, v in enumerate(servers) }

db_nodes = ['cims_cuda2']
video_dir = './data/'
video_streams = ['test_a.mp4', 'test_b.mp4']
streaming_nodes = {
        video_streams[0] : 'cims_cuda4',
        # video_streams[1] : 'cims_cuda2',
        }

# DB nodes
for node in db_nodes:
    workers[node].create_db_job()

for video, node in streaming_nodes.items():
    workers[node].set_db_ip(f"{addresses[db_nodes[0]]}:{db_port}")
    # Save result video 
    workers[node].create_ingesting_stream_job(join(video_dir, video), video.replace('.mp4', '_res.mp4'))
    
    # Dont save result video 
    # workers[node].create_ingesting_stream_job(join(video_dir, video), video.replace('.mp4', '_res.mp4'))

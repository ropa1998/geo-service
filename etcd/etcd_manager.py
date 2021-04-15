import socket
from uuid import uuid4

import etcd3
from apscheduler.schedulers.background import BackgroundScheduler


class EtcdManager:

    def __init__(self, time_to_live=10, etcd_host='127.0.0.1', etcd_port=2379):
        self.time_to_live = time_to_live
        self.client = etcd3.client(host=etcd_host, port=etcd_port)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.__grant_lease, 'interval', seconds=self.time_to_live)
        self.scheduler.start()

    def __grant_lease(self):
        # TODO make the port passed from a config file
        lease = self.client.lease(self.time_to_live)
        self.client.put('/services/geoService/' + str(uuid4()), socket.gethostbyname(socket.gethostname()) + ":50051",
                        lease=lease)

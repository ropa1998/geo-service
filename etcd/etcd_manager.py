import socket
from uuid import uuid4

import etcd3


class EtcdManager:

    def _init_(self, name, time_to_live=10, etcd_host='etcd', etcd_port=2379):
        self.name = name
        self.time_to_live = time_to_live
        self.client = etcd3.client(host=etcd_host, port=etcd_port)

    def grant_lease(self):
        lease = self.client.lease(self.time_to_live)
        # self.client.put('/services/geoService/' + str(uuid4()), socket.gethostbyname(socket.gethostname()))
        self.client.put('/services/geoService/' + str(uuid4()), socket.gethostbyname(socket.gethostname()), lease=lease)
        while lease.remaining_ttl < 1:
            lease.refresh()

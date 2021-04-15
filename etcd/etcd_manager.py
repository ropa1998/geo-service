import socket
from uuid import uuid4

import etcd3
from apscheduler.schedulers.background import BackgroundScheduler

LEADER_KEY = '/leader'
LEASE_TTL = 5
SLEEP = 1


class EtcdManager:

    def __init__(self, time_to_live=10, etcd_host='127.0.0.1', etcd_port=2379):
        self.time_to_live = time_to_live
        self.leader = False
        self.client = etcd3.client(host=etcd_host, port=etcd_port)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self._grant_lease, 'interval', seconds=self.time_to_live)
        self.scheduler.add_job(self._election, 'interval', seconds=LEASE_TTL)
        self.scheduler.start()

    def is_leader(self):
        return self.leader

    def _grant_lease(self):
        # TODO make the port passed from a config file
        lease = self.client.lease(self.time_to_live)
        self.client.put('/services/geoService/' + str(uuid4()), socket.gethostbyname(socket.gethostname()) + ":50051",
                        lease=lease)

    def _election(self, ip_and_port="127.0.0.1:50051"):
        if self.leader:
            self.lease.refresh()
        else:
            self.leader, self.lease = self._leader_election(ip_and_port)

    def _put_not_exist(self, client, key, value, lease=None):
        status, _ = client.transaction(
            compare=[
                client.transactions.version(key) == 0
            ],
            success=[
                client.transactions.put(key, value, lease)
            ],
            failure=[],
        )
        return status

    def _leader_election(self, me):
        try:
            lease = self.client.lease(LEASE_TTL)
            status = self._put_not_exist(client, LEADER_KEY, me, lease)
        except Exception:
            status = False
            lease = None
        return status, lease

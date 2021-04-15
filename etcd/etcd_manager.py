import socket
import time
from uuid import uuid4
from threading import Event

import etcd3
from apscheduler.schedulers.background import BackgroundScheduler

LEADER_KEY = '/leader/geo'
LEASE_TTL = 5
SLEEP = 1


class EtcdManager:

    def __init__(self, time_to_live=10, etcd_host='127.0.0.1', etcd_port=2379, my_port="50051"):
        self.time_to_live = time_to_live
        self.is_leader = False
        self.leader = ""
        self.my_port = my_port
        self.uuid = str(uuid4())
        self.client = etcd3.client(host=etcd_host, port=etcd_port)
        self.client.add_watch_callback(LEADER_KEY, self.watch_cb)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self._grant_lease, 'interval', seconds=self.time_to_live - 2)
        self.scheduler.add_job(self._election, 'interval', seconds=LEASE_TTL - 2)
        self.scheduler.start()

    def is_leader(self):
        return self.is_leader

    def get_current_leader(self):
        self.leader

    def watch_cb(self, event):
        if isinstance(event.events[0], etcd3.events.DeleteEvent):
            self.is_leader = False

    def _grant_lease(self):
        lease = self.client.lease(self.time_to_live)
        self.client.put('/services/geo/' + self.uuid,
                        self.my_ip_and_port(),
                        lease=lease)

    def my_ip_and_port(self):
        return "localhost" + ":" + self.my_port

    def _election(self):
        if self.is_leader:
            self.lease.refresh()
        else:
            self.is_leader, self.lease = self._leader_election(self.my_ip_and_port())

    def _put_not_exist(self, client, key, value, lease=None):
        status, value = client.transaction(
            compare=[
                client.transactions.version(key) == 0
            ],
            success=[
                client.transactions.put(key, value, lease)
            ],
            failure=[],
        )
        if not status:
            self.leader = client.get(LEADER_KEY)[0].decode("utf-8")
        return status

    def _leader_election(self, me):
        try:
            lease = self.client.lease(LEASE_TTL)
            status = self._put_not_exist(self.client, LEADER_KEY, me, lease)
        except Exception:
            status = False
            lease = None
        return status, lease

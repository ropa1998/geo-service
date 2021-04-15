import socket
from concurrent import futures
from uuid import uuid4
import yaml

import grpc

import geoService_pb2
import geoService_pb2_grpc
from etcd.etcd_manager import EtcdManager
from services.geo_service import GeoService

import etcd3

yamlfile = open("config.yaml", "r")
yaml_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
port = yaml_info["port"]


class GeoServiceServer(geoService_pb2_grpc.GeoServiceServicer):

    def __init__(self):
        self.geo_service = GeoService()
        self.etcd_manager = EtcdManager(my_port=port)

    def GetAllCountries(self, request, context):
        response = geoService_pb2.GetAllCountriesReply()
        response.countries.extend(self.geo_service.get_countries())
        return response

    def GetCities(self, request, context):
        response = geoService_pb2.GetCitiesReply()
        response.cities.extend(self.geo_service.get_cities(request.name))
        return response

    def GetSubCountries(self, request, context):
        response = geoService_pb2.GetSubCountriesReply()
        response.subCountries.extend(self.geo_service.get_states(request.name))
        return response

    def GetLocationOfIp(self, request, context):
        response = geoService_pb2.GetLocationOfIpReply()
        aux = self.get_location_from_ip(request)
        if 'country' in aux and 'state' in aux:
            response.country = aux['country']
            response.state = aux['state']
        else:
            response.error = aux
        return response

    def get_location_from_ip_from_leader(self, direction):
        channel = grpc.insecure_channel(self.etcd_manager.leader)
        stub = geoService_pb2_grpc.GeoServiceStub(channel)
        country = geoService_pb2.Ip(direction=direction)
        response = stub.GetLocationOfIp(country)
        return response

    def get_location_from_ip(self, request):
        response = self.geo_service.get_location_from_ip(request.direction, self.etcd_manager.is_leader)
        if response is None:
            response = self.get_location_from_ip_from_leader(request.direction)
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
geoService_pb2_grpc.add_GeoServiceServicer_to_server(
    GeoServiceServer(), server)
print('Starting server. Listening on port {port}.'.format(port=port))
server.add_insecure_port('[::]:{port}'.format(port=port))
server.start()
server.wait_for_termination()

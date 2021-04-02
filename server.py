from concurrent import futures

import grpc

import geoService_pb2
import geoService_pb2_grpc
from services.geo_service import GeoService


class GeoServiceServer(geoService_pb2_grpc.GeoServiceServicer):

    def __init__(self):
        self.geo_service = GeoService()

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
        aux = self.geo_service.get_location_from_ip(request.direction)
        if 'country' in aux and 'state' in aux:
            response.country = aux['country']
            response.state = aux['state']
        else:
            response.error = aux
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_GeoServiceServicer_to_server`
# to add the defined class to the server
geoService_pb2_grpc.add_GeoServiceServicer_to_server(
        GeoServiceServer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()

# The server start() method is non-blocking.
# A new thread will be instantiated to handle requests.
# The thread calling server.start() will often not have any other work to do in the meantime.
# In this case, you can call server.wait_for_termination() to cleanly block the calling thread until the server terminates.

# # since server.start() will not block,
# # a sleep-loop is added to keep alive
# try:
#     while True:
#         time.sleep(86400)
# except KeyboardInterrupt:
#     server.stop(0)

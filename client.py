# open a gRPC channel
import grpc

import geoService_pb2
import geoService_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = geoService_pb2_grpc.GeoServiceStub(channel)

# create a valid request message
empty = geoService_pb2.Empty()

# make the call
response = stub.GetAllCountries(empty)

# et voilà
print(response.countries)

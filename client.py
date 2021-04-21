# open a gRPC channel
import grpc

import geoService_pb2
import geoService_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = geoService_pb2_grpc.GeoServiceStub(channel)

# create a valid request message
country = geoService_pb2.Ip(direction="13.227.69.56")

# make the call
response = stub.GetLocationOfIp(country)

# et voilà
print(response.country, response.state, response.error)

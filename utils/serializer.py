import json
import base64


class JsonSerde(object):
    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key, value, flags):
       if flags == 1:
           return value
       if flags == 2:
           return json.loads(value)
       raise Exception("Unknown serialization format")


class GrpcSerde(object):
    def serialize(self, key, value):

        if isinstance(value, str):
            return value, 1
        return base64.b64encode(bytes(value, 'utf-8')), 2

    def deserialize(self, key, value, flags):
        if flags == 1:
            return value
        if flags == 2:
            return base64.b64decode(value)
        raise Exception("Unknown serialization format")
from utils.csv_reader import CsvReader
import requests
from pymemcache.client import base

from utils.serializer import JsonSerde, GrpcSerde


class GeoService:

    def __init__(self):
        path = 'data/cities'
        self.csv_reader = CsvReader(path)
        self.cached_ip_address = base.Client('locahost:11211', serde=GrpcSerde())

    def get_countries(self):
        countries = []
        for row in self.csv_reader.data:
            country = row['country']
            if country not in countries:
                countries.append(country)
        return countries

    def get_states(self, country):
        states = []
        for row in self.csv_reader.data:
            if row['country'] == country:
                state = row['subcountry']
                if state not in states:
                    states.append(state)
        return states

    def get_cities(self, state):
        cities = []
        for row in self.csv_reader.data:
            if row['subcountry'] == state:
                city = row['name']
                if city not in cities:
                    cities.append(city)
        return cities

    def get_location_from_ip(self, ip_address, can_request):
        result = self.cached_ip_address.get(ip_address)
        if result is not None:
            return result
        if not can_request:
            return result
        path = 'https://ipapi.co/{ip_address}/json/'.format(ip_address=ip_address)
        r = requests.get(path)
        json_response = r.json()
        if 'error' in json_response:
            error_message = 'INVALID_IP_ADDRESS'
            self.cached_ip_address.set(ip_address, error_message)
            return error_message
        response = dict(country=json_response['country_name'], state=json_response['region'])
        self.cached_ip_address.set(ip_address, response)
        return response

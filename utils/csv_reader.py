import csv


class CsvReader:

    def __init__(self, path):
        data = []
        with open(path, mode='r') as csv_file:
            csv_dict_reader = csv.DictReader(csv_file)
            for row in csv_dict_reader:
                data.append(row)
        self.data = data

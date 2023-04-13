import csv
from trip import Trip

class TripLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load(self):
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            return [Trip(**row) for row in reader]

import csv


class ResultsFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, "r") as f:
            # example row:
            # {
            #   'trip_id': '123_2021-01-01_2021-01-02_2',
            #   'is_available': 'True',
            # }
            reader = csv.DictReader(f)
            return {row["trip_id"]: row["is_available"] for row in reader}

    def write(self, results):
        with open(self.file_path, "w") as f:
            # example results:
            # {
            #   '123_2021-01-01_2021-01-02_2': 'True',
            #   '123_2021-01-01_2021-01-03_2': 'False',
            # }
            writer = csv.writer(f)
            writer.writerow(["trip_id", "is_available"])
            for trip_id, is_available in results.items():
                writer.writerow([trip_id, is_available])

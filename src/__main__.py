import os
from trip import Trip
from file.trip_loader import TripLoader
from file.results_file_io import ResultsFileHandler

def main():
    base_dir = os.path.dirname(__file__)
    # Load trips from file
    trips_file = os.path.join(base_dir, 'config/trips.csv')
    trips = TripLoader(trips_file).load()

    # Get previous results
    results_file = os.path.join(base_dir, 'data/results.csv')
    results_file_handler = ResultsFileHandler(results_file)
    results = results_file_handler.read()
    
    for trip in trips:
        prev_result_for_trip = results.get(trip.trip_id())
        print(f"Checking availability for {trip.room_id}...")

        is_available = trip.is_available()
        results[trip.trip_id()] = is_available

        print(
            f"Room {trip.room_id} is {'not ' if not is_available else ''}"
            f"available for {trip.check_in} to {trip.check_out}"
        )
    
    # Write new results to file
    results_file_handler.write(results)

if __name__ == '__main__':
    main()
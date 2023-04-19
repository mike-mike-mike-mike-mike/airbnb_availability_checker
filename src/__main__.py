import os.path as path
from file.trip_loader import TripLoader
from file.results_file_io import ResultsFileHandler
from util.notifications import NewAvailabilityNotifierFactory
from config import secrets

def main():
    base_dir = path.dirname(__file__)
    # Load trips from file
    trips_file = path.join(base_dir, 'config/trips.csv')
    trips = TripLoader(trips_file).load()

    # Get previous results
    results_file = path.join(base_dir, 'data/results.csv')
    results_file_handler = ResultsFileHandler(results_file)
    results = results_file_handler.read()
    
    notifier = NewAvailabilityNotifierFactory.get_notifier('sms')

    for trip in trips:
        was_previously_available = results.get(trip.trip_id) == 'True'
        print(f"Checking availability for {trip.room_id}...")

        is_available_now = trip.is_available()
        results[trip.trip_id] = is_available_now

        print(
            f"Room {trip.room_id} is {'not ' if not is_available_now else ''}"
            f"available for {trip.check_in} to {trip.check_out}"
        )

        if is_available_now and not was_previously_available:
            print(f"Room {trip.room_id} is now available!")
            print(f"Sending notification to {secrets.notifications_phone_number()}...")
            print(notifier.notify(trip))
    
    # Write new results to file
    results_file_handler.write(results)

if __name__ == '__main__':
    main()
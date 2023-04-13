import os
from trip import Trip
from file.trip_loader import TripLoader

def main():

    # Load trips from file
    trips_file = os.path.join(os.path.dirname(__file__), 'config/trips.csv')
    trips = TripLoader(trips_file).load()

    # Check availability for each trip
    results = []
    for trip in trips:
        print(f"Checking availability for {trip.room_id}...")
        is_available = trip.is_available()
        results.append(
            f"Room {trip.room_id} is {'not ' if not is_available else ''}"
            "available for {trip.check_in} to {trip.check_out}"
        )
    
    print(results)

if __name__ == '__main__':
    main()
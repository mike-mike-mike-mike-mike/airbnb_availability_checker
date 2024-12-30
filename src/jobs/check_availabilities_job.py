from file.logger import Logger
from file.project_paths import LOG_FILE, RESULTS_FILE, TRIPS_FILE
from file.trip_loader import TripLoader
from file.results_file_io import ResultsFileHandler
from util.notifications import NewAvailabilityNotifierFactory
from config import secrets
from web.trip_page_parser import TripPageParserFactory


class CheckAvailabilitiesJob:
    def perform(self):
        trips = TripLoader(TRIPS_FILE).load()
        trip_page_parser = TripPageParserFactory.get_parser(
            TripPageParserFactory.ParserType.PLAYWRIGHT
        )
        logger = Logger(LOG_FILE)
        results_file_handler = ResultsFileHandler(RESULTS_FILE)
        results = results_file_handler.read()
        notifier = NewAvailabilityNotifierFactory.get_notifier(
            NewAvailabilityNotifierFactory.NotifierType.CONSOLE
        )

        for trip in trips:
            was_previously_available = results.get(trip.trip_id) == "True"
            print(f"Checking availability for {trip.room_id}...")
            logger.log(f"Checking availability for {trip.room_id}...")

            is_available_now, room_name = trip_page_parser.parse(trip)
            results[trip.trip_id] = is_available_now

            print(
                f"{room_name} is {'not ' if not is_available_now else ''}"
                f"available for {trip.check_in} to {trip.check_out}"
            )
            logger.log(
                f"{room_name} is {'not ' if not is_available_now else ''}"
                f"available for {trip.check_in} to {trip.check_out}"
            )

            if is_available_now and not was_previously_available:
                print(f"{room_name} is now available!")
                print(
                    f"Sending notification to {secrets.notifications_phone_number()}..."
                )
                print(notifier.notify(trip, room_name))

            # Write new results to file
            results_file_handler.write(results)

        trip_page_parser.close()

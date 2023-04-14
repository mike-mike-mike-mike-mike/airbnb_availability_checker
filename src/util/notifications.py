from config import secrets
from twilio.rest import Client

class NewAvailabilityNotifier:
    VALID_NOTIFICATION_METHODS = ['sms', 'email']
    
    def __init__(self, method):
        if method not in self.VALID_NOTIFICATION_METHODS:
            raise ValueError(f"Invalid notification method: {method}")
        self.method = method
        self.client = Client(secrets.twilio_account_sid(), secrets.twilio_auth_token())
    
    def notify(self, trip):
        body = self.__build_body(trip)

        if self.method == 'sms':
            message = self.client.messages.create(
                messaging_service_sid= secrets.twilio_msg_service_sid(),
                to = secrets.notifications_phone_number(),
                body = body
            )
    
            return message.sid
        elif self.method == 'email':
            # TODO
            pass
    
    def __build_body(self, trip):
        # the trial version of twilio is giving me trouble with sending links
        return (
            f"Hey this is your airbnb bot!\n\n"
            f"Your trip to room {trip.room_id} from {trip.check_in} to {trip.check_out} is now available!"
        )
        # return (
        #     f"Hey this is your airbnb bot!\n\n"
        #     f"Room {trip.room_id} is now available for "
        #     f"{trip.check_in} to {trip.check_out}! "
        #     f"Book now at {trip.url}!"
        # )

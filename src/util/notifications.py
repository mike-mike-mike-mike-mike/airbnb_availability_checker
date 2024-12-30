from config import secrets
from twilio.rest import Client
from email.message import EmailMessage
from email.utils import formataddr


class BaseNotifier:
    def notify(self, _trip, _room_name):
        raise NotImplementedError("Subclasses must implement this method")

    def _build_body(self, trip, room_name):
        return (
            f"Hey this is your airbnb bot!\n\n"
            f"'{room_name}' is now available for {trip.check_in} to {trip.check_out}! "
            f"Book now at {trip.url}!"
        )


class ConsoleNotifier(BaseNotifier):
    def notify(self, trip, room_name):
        print(super()._build_body(trip, room_name))


# class EmailNotifier(BaseNotifier):
#     def notify(self, trip):
#         email_address = secrets.notifications_email()
#         to = email_address
#         subject = 'The Airbnb you are watching is now available!'
#         body = super()._build_body(trip)

#         from_name = 'Airbnb Availability Bot'
#         from_email = email_address
#         password = secrets.notifications_email_password()

#         msg = EmailMessage()
#         msg.set_content(body)
#         msg['To'] = to
#         msg['Subject'] = subject
#         msg['From'] = formataddr((from_name, from_email))

#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             smtp.login(from_email, password)
#             smtp.send_message(msg)


class SMSNotifier(BaseNotifier):
    def __init__(self):
        self.client = Client(secrets.twilio_account_sid(), secrets.twilio_auth_token())
        self.messaging_service_sid = secrets.twilio_msg_service_sid()
        self.notifications_phone_number = secrets.notifications_phone_number()

    def notify(self, trip, room_name):
        body = self._build_body(trip, room_name)

        message = self.client.messages.create(
            messaging_service_sid=self.messaging_service_sid,
            to=self.notifications_phone_number,
            body=body,
        )

        return message.sid

    def _build_body(self, trip, room_name):
        # the trial version of twilio is giving me trouble with sending links
        return (
            f"Hey this is your airbnb bot!\n\n"
            f"'{room_name}' is now available for {trip.check_in} to {trip.check_out}! "
            f"Room ID: {trip.room_id}"
        )


class NewAvailabilityNotifierFactory:
    class NotifierType:
        SMS = "sms"
        EMAIL = "email"
        CONSOLE = "console"

    @staticmethod
    def get_notifier(method):
        if method == NewAvailabilityNotifierFactory.NotifierType.SMS:
            return SMSNotifier()
        elif method == NewAvailabilityNotifierFactory.NotifierType.EMAIL:
            # return EmailNotifier()
            pass
        elif method == NewAvailabilityNotifierFactory.NotifierType.CONSOLE:
            return ConsoleNotifier()
        else:
            raise ValueError(f"Invalid notification method: {method}")

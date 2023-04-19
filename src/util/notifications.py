from config import secrets
from twilio.rest import Client
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

class BaseNotifier:
    def notify(self, _trip):
        raise NotImplementedError("Subclasses must implement this method")
    
    def _build_body(self, trip):
        return (
            f"Hey this is your airbnb bot!\n\n"
            f"'{trip.room_name}' is now available for {trip.check_in} to {trip.check_out}! "
            f"Book now at {trip.url}!"
        )
    
class ConsoleNotifier(BaseNotifier):
    def notify(self, trip):
        print(super()._build_body(trip))

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
    def notify(self, trip):
        client =  Client(secrets.twilio_account_sid(), secrets.twilio_auth_token())
        messaging_service_sid = secrets.twilio_msg_service_sid()
        notifications_phone_number = secrets.notifications_phone_number()
        body = self._build_body(trip)

        message = client.messages.create(
            messaging_service_sid= messaging_service_sid,
            to = notifications_phone_number,
            body = body
        )

        return message.sid
    
    def _build_body(self, trip):
        # the trial version of twilio is giving me trouble with sending links
        return (
            f"Hey this is your airbnb bot!\n\n"
            f"'{trip.room_name}' is now available for {trip.check_in} to {trip.check_out}! "
            f"Room ID: {trip.room_id}"
        )

class NewAvailabilityNotifierFactory:
    VALID_NOTIFICATION_METHODS = ['sms', 'email', 'console']

    @staticmethod
    def get_notifier(method):
        if method == 'sms':
            return SMSNotifier()
        elif method == 'email':
            # return EmailNotifier()
            pass
        elif method == 'console':
            return ConsoleNotifier()
        else:
            raise ValueError(f"Invalid notification method: {method}")

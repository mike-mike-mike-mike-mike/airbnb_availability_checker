from dotenv import dotenv_values
from functools import lru_cache
import os.path as path

@lru_cache(maxsize=None)
def secrets():
  dotenv_path = path.join(path.dirname(__file__), '.env')
  return dotenv_values(dotenv_path)

def twilio_account_sid():
  return secrets()['TWILIO_ACCOUNT_SID']

def twilio_auth_token():
  return secrets()['TWILIO_AUTH_TOKEN']

def twilio_msg_service_sid():
  return secrets()['TWILIO_MSG_SERVICE_SID']

def notifications_phone_number():
  return secrets()['NOTIFICATIONS_PHONE_NUMBER']
    
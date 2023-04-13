from util.url_builder import UrlBuilder
from web.availability_checker import AvailablityChecker

class Trip:
    def __init__(self, room_id, check_in, check_out, guests = 2):
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.guests = guests
    
    def is_available(self):
        return AvailablityChecker(self.__url()).check_availability()

    def __url(self):
        return UrlBuilder(self.room_id, self.check_in, self.check_out, self.guests).build()
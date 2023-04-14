from util.url_builder import UrlBuilder
from web.availability_checker import AvailablityChecker

class Trip:
    def __init__(self, room_id, check_in, check_out):
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.url = self.__url()
        self.trip_id = self.__trip_id()
    
    def is_available(self):
        return AvailablityChecker(self.url).check_availability()
    
    def __trip_id(self):
        return f'{self.room_id}_{self.check_in}_{self.check_out}'
    
    def __url(self):
        return UrlBuilder(self.room_id, self.check_in, self.check_out).build()
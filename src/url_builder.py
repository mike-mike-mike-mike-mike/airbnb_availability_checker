class UrlBuilder:
    HOST = 'https://www.airbnb.com/rooms'

    def __init__(self, room_id, check_in, check_out, guests = 2):
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.guests = guests

    def build(self):
        check_in_param = f'check_in={self.check_in}'
        check_out_param = f'check_out={self.check_out}'
        guests_param = f'adults={self.guests}'

        return f'{self.HOST}/{self.room_id}?{check_in_param}&{check_out_param}&{guests_param}'
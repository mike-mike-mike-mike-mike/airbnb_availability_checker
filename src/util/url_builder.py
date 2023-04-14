class UrlBuilder:
    HOST = 'https://www.airbnb.com/rooms'

    def __init__(self, room_id, check_in, check_out):
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out

    # e.g. https://www.airbnb.com/rooms/50617365?check_in=2023-07-02&check_out=2023-07-06
    def build(self):
        check_in_param = f'check_in={self.check_in}'
        check_out_param = f'check_out={self.check_out}'

        return f'{self.HOST}/{self.room_id}?{check_in_param}&{check_out_param}'

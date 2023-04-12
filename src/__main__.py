from util.url_builder import UrlBuilder
from web.availability_checker import AvailablityChecker

def main():
    # i.e. https://www.airbnb.com/rooms/50617365?check_in=2023-07-02&check_out=2023-07-06&adults=2
    room_url = UrlBuilder('50617365', '2023-07-02', '2023-07-06').build()
    is_available = AvailablityChecker(room_url).check_availability()

    print(f"The room is {'not ' if not is_available else ''}available for those dates")

if __name__ == '__main__':
    main()
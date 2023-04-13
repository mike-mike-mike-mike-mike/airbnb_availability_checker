from trip import Trip

def main():
    # i.e. https://www.airbnb.com/rooms/50617365?check_in=2023-07-02&check_out=2023-07-06&adults=2
    trip = Trip('50617365', '2023-07-02', '2023-07-06')
    is_available = trip.is_available()

    print(f"The room is {'not ' if not is_available else ''}available for those dates")

if __name__ == '__main__':
    main()
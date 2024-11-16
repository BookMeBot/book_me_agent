from src.travala_booking import BookingRequest, GuestInfo, TravalaBooker


def test_booking():
    # Create test booking request
    guest_info = GuestInfo(
        first_name="Marissa",
        last_name="Posner",
        phone_number="(+66) 0992930723",
        email="marissa@gold.dev",
        bedding_preference="2 Twin Beds",
    )

    booking_request = BookingRequest(
        location="Chiang Mai, Chiang Mai Province, Thailand",
        check_in="27 Nov 2024",
        check_out="28 Nov 2024",
        guests=2,
        guest_info=guest_info,
        max_price=30.0,
    )

    try:
        booker = TravalaBooker()
        result = booker.book_hotel(booking_request)
        print("Booking Result:", result)
    except Exception as e:
        print("Booking Error:", str(e))


if __name__ == "__main__":
    test_booking()

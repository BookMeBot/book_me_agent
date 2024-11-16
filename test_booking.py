from src.travala_booking import BookingRequest, GuestInfo, TravalaBooker
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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
        location="Chiang Mai, Thailand",  # Simplified location
        check_in="27 Nov 2024",
        check_out="28 Nov 2024",
        guests=2,
        guest_info=guest_info,
        max_price=30.0,
    )

    try:
        logger.info("Starting booking test...")
        logger.info(f"Booking details: {booking_request}")

        booker = TravalaBooker()
        result = booker.book_hotel(booking_request)

        logger.info(f"Booking Result: {result}")
        return result

    except Exception as e:
        logger.error(f"Booking Error: {str(e)}")
        return None


if __name__ == "__main__":
    test_booking()

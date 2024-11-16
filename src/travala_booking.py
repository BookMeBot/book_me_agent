from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


class GuestInfo(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    bedding_preference: str = "2 Twin Beds"


class BookingRequest(BaseModel):
    location: str
    check_in: str
    check_out: str
    guests: int
    guest_info: GuestInfo
    max_price: Optional[float] = None


class TravalaBooker:
    def __init__(self):
        self.default_timeout = 60000  # 60 seconds

    def wait_and_click(self, page, selector: str, timeout: int = None) -> bool:
        """Helper method to wait for element and click it"""
        try:
            timeout = timeout or self.default_timeout
            element = page.wait_for_selector(selector, timeout=timeout, state="visible")
            if element:
                element.click()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {str(e)}")
            return False

    def search_hotel(self, page, booking_request: BookingRequest) -> bool:
        """Search for hotels with given criteria"""
        try:
            # Navigate to homepage
            logger.info("Navigating to Travala.com...")
            page.goto("https://www.travala.com/")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_load_state("networkidle")

            # Wait for React app to be fully loaded
            page.wait_for_selector('div[role="main"]', timeout=self.default_timeout)
            page.wait_for_timeout(3000)  # Additional wait for React initialization

            # Handle location input
            logger.info("Entering location...")
            location_selectors = [
                'input[placeholder*="Where are you going?"]',
                'input[type="search"]',
                '[data-testid="search-location-input"]',
            ]

            location_input = None
            for selector in location_selectors:
                try:
                    location_input = page.wait_for_selector(
                        selector, timeout=5000, state="visible"
                    )
                    if location_input:
                        break
                except Exception:
                    continue

            if not location_input:
                raise Exception("Location input not found")

            # Clear and fill location
            location_input.click()
            location_input.fill("")
            page.keyboard.type(booking_request.location, delay=100)
            page.wait_for_timeout(2000)

            # Try to select from autocomplete
            try:
                page.click(".suggestion-item", timeout=5000)
            except:
                location_input.press("Enter")

            page.wait_for_timeout(1000)

            # Handle dates
            logger.info("Setting dates...")

            # Click date input
            date_button = page.wait_for_selector(
                '[data-testid="search-date-input"]', timeout=5000
            )
            if date_button:
                date_button.click()
                page.wait_for_timeout(1000)

                # Select check-in date
                page.locator(f'text="{booking_request.check_in}"').first.click()
                page.wait_for_timeout(1000)

                # Select check-out date
                page.locator(f'text="{booking_request.check_out}"').first.click()
                page.wait_for_timeout(1000)

            # Handle guests
            logger.info("Setting guest count...")
            guests_button = page.wait_for_selector(
                '[data-testid="search-guest-input"]', timeout=5000
            )
            if guests_button:
                guests_button.click()
                page.wait_for_timeout(1000)

                # Adjust guest count
                current_guests = 2
                while current_guests < booking_request.guests:
                    page.click('button:has-text("+")')
                    current_guests += 1
                    page.wait_for_timeout(500)

            # Click search
            logger.info("Initiating search...")
            search_button = page.wait_for_selector(
                'button:has-text("SEARCH")', timeout=5000
            )
            if search_button:
                search_button.click()
                page.wait_for_timeout(1000)

            # Wait for results page
            logger.info("Waiting for search results...")
            try:
                page.wait_for_selector(".hotel-list", timeout=self.default_timeout)
                page.wait_for_load_state("networkidle")
                logger.info("Search results loaded successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to load search results: {str(e)}")
                page.screenshot(path="search_results_error.png")
                raise

        except Exception as e:
            logger.error(f"Search hotel error: {str(e)}")
            page.screenshot(path=f"error_{time.strftime('%Y%m%d_%H%M%S')}.png")
            raise

    def book_hotel(self, booking_request: BookingRequest):
        """Main booking function"""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    "--start-maximized",
                ],
                timeout=60000,
            )

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            )

            # Add error handling for React errors
            context.route("**/*", lambda route: route.continue_())
            page = context.new_page()

            try:
                # Navigate and search
                search_success = self.search_hotel(page, booking_request)

                if search_success:
                    logger.info("Search completed successfully")
                    # Additional booking steps would go here
                    return {"status": "success", "message": "Search completed"}
                else:
                    raise Exception("Search failed")

            except Exception as e:
                logger.error(f"Booking failed: {str(e)}")
                raise
            finally:
                page.close()
                context.close()
                browser.close()


@app.post("/book")
async def book_hotel_endpoint(booking_request: BookingRequest):
    try:
        booker = TravalaBooker()
        result = booker.book_hotel(booking_request)
        return {"status": "success", "booking_details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

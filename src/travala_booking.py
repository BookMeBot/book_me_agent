from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
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
    max_price: float = None


class TravalaBooker:
    def search_hotel(self, page, booking_request):
        """Search for hotels with given criteria"""
        try:
            logger.info(f"Starting hotel search for {booking_request.location}")

            # Navigate to homepage with longer timeout
            logger.info("Navigating to Travala.com...")
            page.goto("https://www.travala.com/", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            # Ensure the page is fully loaded
            logger.info("Waiting for page to be fully loaded...")
            try:
                # Wait for the main search container
                page.wait_for_selector('.hero-section', timeout=30000)
                logger.info("Main search container found")
            except Exception as e:
                logger.error("Could not find main search container")
                page.screenshot(path="missing_search_container.png")
                raise

            # Add a small delay to ensure JavaScript is loaded
            page.wait_for_timeout(2000)

            # Try to find the search input using multiple selectors
            logger.info("Looking for search input...")
            location_input = None
            selectors = [
                'input[placeholder*="Where are you going?"]',
                '[data-testid="search-location-input"]',
                'input[type="text"]'
            ]
            
            for selector in selectors:
                try:
                    location_input = page.wait_for_selector(selector, timeout=5000, state='visible')
                    if location_input:
                        logger.info(f"Found input using selector: {selector}")
                        break
                except Exception:
                    continue

            if not location_input:
                logger.error("Could not find location input")
                page.screenshot(path="no_location_input.png")
                raise Exception("Location input not found")

            # Click and fill location with retry
            for attempt in range(3):
                try:
                    # Clear any existing text
                    location_input.evaluate('(el) => el.value = ""')
                    location_input.click(timeout=5000)
                    
                    # Type slowly
                    for char in booking_request.location:
                        location_input.type(char, timeout=1000)
                        page.wait_for_timeout(100)
                    
                    logger.info("Location entered successfully")
                    page.wait_for_timeout(2000)
                    
                    # Try to select from dropdown if available
                    try:
                        page.click('.suggestion-item >> nth=0', timeout=5000)
                    except:
                        location_input.press('Enter')
                    
                    break
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == 2:
                        raise
                    page.wait_for_timeout(1000)

            # Handle dates
            logger.info("Setting dates...")
            try:
                # Try different date picker selectors
                date_selectors = [
                    '[data-testid="search-date-input"]',
                    '.date-picker-input',
                    'input[placeholder*="Check-in"]'
                ]
                
                date_picker = None
                for selector in date_selectors:
                    try:
                        date_picker = page.wait_for_selector(selector, timeout=5000)
                        if date_picker:
                            break
                    except:
                        continue
                
                if date_picker:
                    date_picker.click(timeout=5000)
                    page.wait_for_timeout(1000)
                    
                    # Click check-in date
                    if not page.click(f'text="{booking_request.check_in}"', timeout=5000):
                        logger.error("Could not click check-in date")
                        raise Exception("Check-in date not found")
                    
                    page.wait_for_timeout(1000)
                    
                    # Click check-out date
                    if not page.click(f'text="{booking_request.check_out}"', timeout=5000):
                        logger.error("Could not click check-out date")
                        raise Exception("Check-out date not found")
                else:
                    raise Exception("Date picker not found")
                    
            except Exception as e:
                logger.error(f"Date selection failed: {str(e)}")
                page.screenshot(path="date_selection_error.png")
                raise

            # Handle guests
            logger.info("Setting guest count...")
            try:
                guests_selectors = [
                    '[data-testid="search-guest-input"]',
                    '.guest-input',
                    'div[role="button"]:has-text("guests")'
                ]
                
                guests_input = None
                for selector in guests_selectors:
                    try:
                        guests_input = page.wait_for_selector(selector, timeout=5000)
                        if guests_input:
                            break
                    except:
                        continue
                
                if guests_input:
                    guests_input.click(timeout=5000)
                    page.wait_for_timeout(1000)
                    
                    # Update guest count
                    current_guests = 2  # Default value
                    while current_guests < booking_request.guests:
                        page.click('button:has-text("+")', timeout=5000)
                        current_guests += 1
                        page.wait_for_timeout(500)
                else:
                    raise Exception("Guests input not found")
                    
            except Exception as e:
                logger.error(f"Guest selection failed: {str(e)}")
                page.screenshot(path="guest_selection_error.png")
                raise

            # Click search with retry
            logger.info("Clicking search button...")
            search_button = None
            search_selectors = [
                'button:has-text("SEARCH")',
                '[data-testid="search-button"]',
                '.search-button'
            ]
            
            for selector in search_selectors:
                try:
                    search_button = page.wait_for_selector(selector, timeout=5000)
                    if search_button:
                        break
                except:
                    continue

            if search_button:
                search_button.click(timeout=5000)
                logger.info("Search button clicked")
            else:
                logger.error("Search button not found")
                page.screenshot(path="no_search_button.png")
                raise Exception("Search button not found")

            # Wait for results
            logger.info("Waiting for search results...")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(5000)

            # Take screenshot of final state
            page.screenshot(path="search_results.png")

            if page.url != "https://www.travala.com/":
                logger.info("Successfully navigated to search results")
                return True
            else:
                raise Exception("Failed to navigate to search results")

        except Exception as e:
            logger.error(f"Search hotel error: {str(e)}")
            page.screenshot(path=f"error_{time.strftime('%Y%m%d_%H%M%S')}.png")
            raise Exception(f"Search hotel error: {str(e)}")
    def select_first_hotel(self, page):
        """Select the first available hotel from search results"""
        try:
            logger.info("Attempting to select first hotel...")

            # Wait for hotel cards to be visible
            page.wait_for_selector(".hotel-card", timeout=10000)

            # Click the first hotel card
            first_hotel = page.locator(".hotel-card").first
            if first_hotel:
                first_hotel.click()
                page.wait_for_load_state("networkidle")
                time.sleep(2)

                # Click Book Now if available
                book_now = page.locator('button:has-text("Book Now")').first
                if book_now:
                    book_now.click()
                    page.wait_for_load_state("networkidle")

                logger.info("Successfully selected first hotel")
                return True
            else:
                raise Exception("No hotels found in search results")

        except Exception as e:
            logger.error(f"Select hotel error: {str(e)}")
            raise Exception(f"Select hotel error: {str(e)}")

    def fill_guest_info(self, page, guest_info: GuestInfo):
        """Fill in guest information"""
        try:
            logger.info("Filling guest information...")

            # Wait for the form to be visible
            page.wait_for_selector('input[placeholder*="First name"]', timeout=5000)

            # Fill in the form fields
            page.fill('input[placeholder*="First name"]', guest_info.first_name)
            page.fill('input[placeholder*="Last name"]', guest_info.last_name)
            page.fill('input[placeholder*="Phone number"]', guest_info.phone_number)
            page.fill('input[placeholder*="Email"]', guest_info.email)

            # Handle bedding preference
            if guest_info.bedding_preference == "2 Twin Beds":
                page.click('label:has-text("2 Twin Beds")')
            else:
                page.click('label:has-text("1 Double Bed")')

            time.sleep(1)
            logger.info("Guest information filled successfully")

        except Exception as e:
            logger.error(f"Fill guest info error: {str(e)}")
            raise Exception(f"Fill guest info error: {str(e)}")

    def handle_payment(self, page):
        """Handle the payment process"""
        try:
            logger.info("Setting up payment...")

            # Click My Wallet payment method
            my_wallet = page.locator('text="My Wallet"').first
            if my_wallet:
                my_wallet.click()
                time.sleep(1)

            # Select USDC
            page.click('text="USDC USD Coin"')
            time.sleep(1)

            # Select Ethereum network
            page.click('text="Ethereum (ERC20)"')
            time.sleep(1)

            # Get deposit address
            deposit_address = page.text_content(".deposit-address")
            logger.info(f"USDC deposit address: {deposit_address}")

            # Click Complete Reservation
            complete_reservation = page.locator('text="Complete Reservation"').first
            if complete_reservation:
                complete_reservation.click()
                time.sleep(2)

            logger.info("Payment process completed")
            return True

        except Exception as e:
            logger.error(f"Payment error: {str(e)}")
            raise Exception(f"Payment error: {str(e)}")

    def book_hotel(self, booking_request: BookingRequest):
        """Main booking function"""
        with sync_playwright() as p:
            # Launch browser with specific configurations
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--start-maximized',
                    '--disable-notifications',
                    '--disable-geolocation',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ],
                timeout=60000  # Increase browser launch timeout
            )
            
            # Create context with specific viewport and permissions
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                permissions=['geolocation'],
                ignore_https_errors=True,
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            try:
                # Enable better logging
                page.on('console', lambda msg: logger.info(f'Browser console: {msg.text}'))
                page.on('pageerror', lambda err: logger.error(f'Browser error: {err}'))
                
                # Execute booking flow
                if self.search_hotel(page, booking_request):
                    if self.select_first_hotel(page):
                        self.fill_guest_info(page, booking_request.guest_info)
                        self.handle_payment(page)
                        
                        booking_details = {
                            "hotel_name": page.text_content(".hotel-name"),
                            "total_price": page.text_content(".final-price"),
                            "check_in": booking_request.check_in,
                            "check_out": booking_request.check_out,
                            "guests": booking_request.guests,
                            "status": "completed"
                        }
                        
                        logger.info("Booking completed successfully")
                        return booking_details
                
            except Exception as e:
                logger.error(f"Booking failed: {str(e)}")
                page.screenshot(path=f"error_final_{time.strftime('%Y%m%d_%H%M%S')}.png")
                raise Exception(f"Booking failed: {str(e)}")
            
            finally:
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from playwright.sync_api import sync_playwright
import logging
from typing import List, Dict
import json
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TravalaSearcher:
    def __init__(self):
        self.hotels = []
        self.max_pages = 3  # Limit number of pages to search

    def extract_hotel_data(self, page) -> List[Dict]:
        """Extract data from current page of hotel results"""
        hotels_on_page = []

        # Wait for hotel cards to be visible
        page.wait_for_selector(".hotel-card", timeout=10000)

        # Get all hotel cards on the page
        hotel_cards = page.query_selector_all(".hotel-card")

        for card in hotel_cards:
            try:
                hotel_data = {
                    "name": card.query_selector(".hotel-name").text_content().strip(),
                    "price": card.query_selector(".price").text_content().strip(),
                    "rating": card.query_selector(".rating-score")
                    .text_content()
                    .strip(),
                    "location": card.query_selector(".location").text_content().strip(),
                    "url": card.query_selector("a").get_attribute("href"),
                }
                hotels_on_page.append(hotel_data)
                logger.info(f"Found hotel: {hotel_data['name']}")
            except Exception as e:
                logger.error(f"Error extracting hotel data: {str(e)}")
                continue

        return hotels_on_page

    def search_hotels(
        self, location: str, check_in: str, check_out: str, guests: int = 2
    ) -> List[Dict]:
        """Search hotels with pagination"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()

            try:
                # Navigate to Travala
                logger.info(f"Searching for hotels in {location}")
                page.goto("https://www.travala.com/")
                page.wait_for_load_state("networkidle")

                # Fill search criteria
                # Location
                page.click('input[placeholder*="Where are you going?"]')
                page.fill('input[placeholder*="Where are you going?"]', location)
                page.wait_for_timeout(2000)
                page.keyboard.press("Enter")

                # Dates
                page.click('[data-testid="search-date-input"]')
                page.click(f'text="{check_in}"')
                page.wait_for_timeout(500)
                page.click(f'text="{check_out}"')

                # Guests
                page.click('[data-testid="search-guest-input"]')
                current_guests = 2
                while current_guests < guests:
                    page.click('button:has-text("+")')
                    current_guests += 1
                    page.wait_for_timeout(500)

                # Search
                page.click('button:has-text("SEARCH")')
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(5000)  # Wait for results to load

                # Handle pagination
                current_page = 1
                while current_page <= self.max_pages:
                    logger.info(f"Processing page {current_page}")

                    # Extract hotels from current page
                    hotels_found = self.extract_hotel_data(page)
                    self.hotels.extend(hotels_found)
                    logger.info(
                        f"Found {len(hotels_found)} hotels on page {current_page}"
                    )

                    # Check for next page button
                    next_button = page.query_selector('button[aria-label="Next page"]')
                    if not next_button or not next_button.is_enabled():
                        logger.info("No more pages available")
                        break

                    # Click next page
                    next_button.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000)  # Wait for new results

                    current_page += 1

                # Save results to file
                self.save_results()

                return self.hotels

            except Exception as e:
                logger.error(f"Error during search: {str(e)}")
                page.screenshot(path="error.png")
                raise

            finally:
                browser.close()

    def save_results(self):
        """Save search results to JSON file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"hotel_results_{timestamp}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.hotels, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")


def main():
    searcher = TravalaSearcher()

    # Search parameters
    search_params = {
        "location": "Bangkok, Thailand",
        "check_in": "27 Nov 2024",
        "check_out": "28 Nov 2024",
        "guests": 2,
    }

    try:
        hotels = searcher.search_hotels(**search_params)
        logger.info(f"Total hotels found: {len(hotels)}")

        # Print first few results
        for i, hotel in enumerate(hotels[:5], 1):
            print(f"\nHotel {i}:")
            print(f"Name: {hotel['name']}")
            print(f"Price: {hotel['price']}")
            print(f"Rating: {hotel['rating']}")
            print(f"Location: {hotel['location']}")

    except Exception as e:
        logger.error(f"Search failed: {str(e)}")


if __name__ == "__main__":
    main()

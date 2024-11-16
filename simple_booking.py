from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(playwright):
    # Launch the browser
    browser = playwright.chromium.launch(
        headless=False, slow_mo=1000
    )  # slow_mo adds delay to see actions
    page = browser.new_page()

    try:
        # Go to Travala
        logger.info("Navigating to Travala...")
        page.goto("https://www.travala.com/")

        # Wait for the page to load
        page.wait_for_load_state("networkidle")

        # Debug: Take screenshot
        page.screenshot(path="start.png")

        # Fill in location
        logger.info("Filling location...")
        # Click the search box first
        page.click('input[placeholder*="Where are you going?"]')
        # Type the location
        page.fill('input[placeholder*="Where are you going?"]', "Bangkok")
        # Wait a bit for suggestions
        page.wait_for_timeout(2000)
        # Press Enter to select
        page.keyboard.press("Enter")

        # Debug: Take screenshot
        page.screenshot(path="after_location.png")

        # Click date picker
        logger.info("Selecting dates...")
        page.click('[data-testid="search-date-input"]')

        # Select dates
        page.click('text="27 Nov 2024"')  # Check-in
        page.wait_for_timeout(500)
        page.click('text="28 Nov 2024"')  # Check-out

        # Debug: Take screenshot
        page.screenshot(path="after_dates.png")

        # Handle guests
        logger.info("Setting guests...")
        page.click('[data-testid="search-guest-input"]')
        # Default is 2 guests, add more if needed
        # page.click('button:has-text("+")')

        # Click Search
        logger.info("Clicking search...")
        page.click('button:has-text("SEARCH")')

        # Wait for results
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)  # Extra wait to ensure results load

        # Debug: Take screenshot
        page.screenshot(path="results.png")

        # Click first hotel
        logger.info("Selecting first hotel...")
        page.click(".hotel-card >> nth=0")

        # Wait for hotel page
        page.wait_for_load_state("networkidle")

        logger.info("Navigation complete!")

        # Keep browser open for inspection
        input("Press Enter to close browser...")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        page.screenshot(path=f"error.png")
        raise e

    finally:
        browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()

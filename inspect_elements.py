from playwright.sync_api import sync_playwright
import time


def inspect_elements():
    with sync_playwright() as p:
        # Launch browser in non-headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Travala
        page.goto("https://www.travala.com/")
        page.wait_for_load_state("networkidle")

        # Print helpful information about elements
        print("\nInspecting Elements...")

        # Check search input
        search_input = page.query_selector('input[placeholder*="Where are you going?"]')
        if search_input:
            print("\nFound search input:")
            print(search_input.evaluate("el => el.outerHTML"))

        # Check date picker
        date_picker = page.query_selector('[data-testid="search-date-input"]')
        if date_picker:
            print("\nFound date picker:")
            print(date_picker.evaluate("el => el.outerHTML"))

        # Check guest selector
        guest_selector = page.query_selector('[data-testid="search-guest-input"]')
        if guest_selector:
            print("\nFound guest selector:")
            print(guest_selector.evaluate("el => el.outerHTML"))

        # Check search button
        search_button = page.query_selector('button:has-text("SEARCH")')
        if search_button:
            print("\nFound search button:")
            print(search_button.evaluate("el => el.outerHTML"))

        print("\nKeeping browser open for inspection...")
        print("Press Ctrl+C to close")

        # Keep browser open for manual inspection
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")
        finally:
            browser.close()


if __name__ == "__main__":
    inspect_elements()

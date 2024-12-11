from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
import csv

chromium_path = r"C:\Users\gmedh\OneDrive\Documents\chrome-win\chrome-win\chrome.exe"

async def scroll_to_load_all(page):
    previous_height = None
    while True:
        current_height = await page.evaluate('document.body.scrollHeight')
        if previous_height == current_height:
            break  # No more content to load
        previous_height = current_height
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)  # Allow time for content to load

async def fetch_car_listings(url):
    try:
        # Launch browser
        browser = await launch(executablePath=chromium_path, headless=False)
        page = await browser.newPage()
        await page.goto(url, timeout=60000)
        await page.setViewport({'width': 1280, 'height': 800})

        # Infinite scroll to load all cars
        await scroll_to_load_all(page)

        # Extract page content
        content = await page.content()
        await browser.close()
ga
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    except Exception as e:
        print(f"Error fetching car listings: {e}")
        return None

async def extract_and_save_data():
    url = "https://sylndr.com/en/buy-used-cars"
    soup = await fetch_car_listings(url)

    if soup:
        car_cards = soup.select("div[id^='cardofcar']")  # Select all car cards using ID pattern
        car_data = []

        for car in car_cards:
            title = car.select_one("p.car-card-title").get_text(strip=True) if car.select_one("p.car-card-title") else "N/A"

            # Check for discount or no-discount class and extract price
            if "has-discount" in car["class"]:
                price = car.select_one("div.has-discount\\:flex.no-discount\\:hidden p.styles_subtitle1SemiBold__KT9qX").get_text(strip=True)
            elif "no-discount" in car["class"]:
                price = car.select_one("div.no-discount\\:flex.has-discount\\:hidden p.styles_subtitle1SemiBold__KT9qX").get_text(strip=True)
            else:
                price = "N/A"

            # Extract description
            description = car.select_one("p.styles_body2__Z9WUR.car-card-trim-container").get_text(strip=True) if car.select_one("p.styles_body2__Z9WUR.car-card-trim-container") else "N/A"

            # Extract transmission
            transmission = (
                car.select("div.flex.items-center.flex-wrap.gap-2.mt-2 p.styles_body2__Z9WUR")[-1].get_text(strip=True)
                if car.select("div.flex.items-center.flex-wrap.gap-2.mt-2 p.styles_body2__Z9WUR")
                else "N/A"
            )

            # Extract kilometers
            kilometers = car.select_one("div.flex.items-center.flex-wrap.gap-2.mt-2 p.styles_body2__Z9WUR:nth-of-type(1)").get_text(strip=True) if car.select_one("div.flex.items-center.flex-wrap.gap-2.mt-2 p.styles_body2__Z9WUR:nth-of-type(1)") else "N/A"

            car_data.append({
                "Title": title,
                "Price": price,
                "Description": description,
                "Transmission": transmission,
                "Kilometers": kilometers
            })

        # Save data to CSV
        if car_data:
            keys = car_data[0].keys()
            with open('Sylndr_car_listings.csv', 'w', newline='', encoding='utf-8') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(car_data)
            print(f"Saved {len(car_data)} car listings to 'Sylndr_car_listings.csv'.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(extract_and_save_data())

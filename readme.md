# Sylndr Car Listings Scraper

A Python web scraper that extracts car listings data from Sylndr.com (a used car marketplace) and saves it to a CSV file.

## What it does

This script automatically:
- Opens the Sylndr.com used cars page
- Performs infinite scrolling to load all available car listings
- Extracts detailed information about each car including:
  - Car title/model
  - Price (handles both discounted and regular prices)
  - Description/trim details
  - Transmission type
  - Kilometers driven
- Saves all data to a CSV file for analysis

## Prerequisites

### Required Python Packages
```bash
pip install beautifulsoup4 pyppeteer asyncio csv
```

### Chrome Browser
- You need Google Chrome installed on your system
- The script currently uses a specific Chrome executable path: `C:\Users\gmedh\OneDrive\Documents\chrome-win\chrome-win\chrome.exe`
- **Important**: Update the `chromium_path` variable in the script to match your Chrome installation

## Setup

1. **Install dependencies**:
   ```bash
   pip install beautifulsoup4 pyppeteer
   ```

2. **Update Chrome path**:
   - Open `script.py`
   - Modify line 6 to point to your Chrome executable:
   ```python
   chromium_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Windows default
   # or
   chromium_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Mac
   ```

3. **Ensure stable internet connection** for web scraping

## Usage

Run the script from your terminal:

```bash
python script.py
```

### What happens when you run it:
1. Chrome browser opens in non-headless mode (you can see it working)
2. The script navigates to Sylndr.com's used cars page
3. It automatically scrolls down to load all car listings (this may take a few minutes)
4. Data extraction begins for each car card
5. Results are saved to `Sylndr_car_listings.csv` in the same directory

## Output

The script creates a CSV file named `Sylndr_car_listings.csv` with the following columns:

| Column | Description |
|--------|-------------|
| Title | Car make, model, and year |
| Price | Current price (handles discounted prices) |
| Description | Car trim and additional details |
| Transmission | Manual or Automatic |
| Kilometers | Total kilometers driven |

## Features

- **Infinite Scroll Support**: Automatically loads all available cars by scrolling to the bottom
- **Price Handling**: Correctly extracts both regular and discounted prices
- **Error Handling**: Gracefully handles missing data fields
- **UTF-8 Encoding**: Properly saves Arabic/international characters
- **Progress Feedback**: Shows how many listings were saved

## Troubleshooting

### Common Issues:

1. **Chrome path error**: Update the `chromium_path` variable to your Chrome installation
2. **Timeout errors**: Increase the timeout value in `page.goto(url, timeout=60000)`
3. **Network issues**: Ensure stable internet connection
4. **Permission errors**: Run with appropriate file write permissions

### Customization:

- **Change target URL**: Modify the `url` variable to scrape different car categories
- **Headless mode**: Change `headless=False` to `headless=True` for background operation
- **Scroll timing**: Adjust `asyncio.sleep(2)` in the scroll function for slower/faster loading

## Technical Details

- **Framework**: Python with asyncio for asynchronous operations
- **Browser Automation**: Pyppeteer (Puppeteer for Python)
- **HTML Parsing**: BeautifulSoup4
- **Output Format**: CSV with UTF-8 encoding
- **Scroll Strategy**: Monitors `document.body.scrollHeight` to detect when all content is loaded

## Notes

- This script is for educational/research purposes
- Respect the website's robots.txt and terms of service
- Consider adding delays between requests to avoid overwhelming the server
- The script currently targets specific CSS selectors that may change if the website updates

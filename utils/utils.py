import requests
import time
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

# Function to handle HTTP requests with retries
def request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            print(f"HTTP error ({e.response.status_code}): {e}")
        except requests.RequestException as e:
            print(f"Request error: {e}")

        # Sleep for a while before retrying
        time.sleep(5)

    # If all retries fail, raise an exception
    raise Exception(f"Failed to retrieve data from {url}")

# Function to generate a bs4 soup element to enable web scraping
def generate_soup(url):
    try:
        response = request_with_retry(url, headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        raise Exception(f"Soup generation error for url --> {url} [ERROR]: {e}")

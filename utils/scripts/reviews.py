from utils.utils import *
import re
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from typing import List, Optional
from db import *


# Function to extract detail of one review
def extract_review_details(element: Tag) -> Optional[Review]:
    try:
        # Extract review_id
        e = element.find("a", {"class": "title"})
        review_id = re.search(r'/review/(.*?)/', e.get("href")).group(1)

        # Extract title
        title = e.text

        # Extract username
        user = element.find("span", {"class": "display-name-link"}).find("a").text

        # Extract rating
        # If rating is not provided put rating as 0 to avoid NULL values
        try:
            rating = int(element.find("span", {"class": "rating-other-user-rating"}).find("span").text)
        except (AttributeError, ValueError):
            rating = 0

        # Extract Content
        content = element.find("div", {"class": "text show-more__control"}).text

        # Extract date
        date_string = element.find("span", {"class": "review-date"}).text
        date = datetime.strptime(date_string, "%d %B %Y")

        return Review(review_id, user, title, rating, content, date)
    except Exception as e:
        print(f"Error while extracting review (id --> {review_id}) [ERROR] {e}")
        return None

# Function to extract details of all reviews of a movie
def extract_movie_reviews(soup: BeautifulSoup, review_count: int) -> List[Optional[Review]]:
    try:
        review_div_list = soup.find_all("div", {"class": "lister-item-content"})
        if len(review_div_list) < review_count:
            # handle dynamic Javascript here
            pass

        review_list = []
        for i in range(min(len(review_div_list), review_count)):
            try:
                review = extract_review_details(review_div_list[i])
                if review:
                    review_list.append(review)
            except Exception as e:
                print(e)

        return review_list
    except Exception as e:
        raise Exception(f"Error extracting reviews: [ERROR] {e}")


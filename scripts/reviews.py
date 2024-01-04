from utils.utils import *
import re
from bs4 import BeautifulSoup, Tag
from typing import List, Optional
from db import *


# Function to extract detail of one review
def extract_review_details(element: Tag, movie_id: str) -> None:
    try:
        
        datastore_object = DataStore()

        # Extract review_id
        e = element.find("a", {"class": "title"})
        review_id = re.search(r'/review/(.*?)/', e.get("href")).group(1)

        # Extract title
        title = e.text

        # Extract user

        username = element.find("span", {"class": "display-name-link"}).find("a").text
        userlink = element.find("span", {"class": "display-name-link"}).find("a").get("href")
        user_id = re.search(r'/user/(.*?)/', userlink).group(1)
        user = User(user_id, username)
        datastore_object.insert_into_users(user)
        datastore_object.commit()
         
        # Extract rating
        # If rating is not provided put rating as 0 to avoid NULL values
        try:
            rating = element.find("span", {"class": "rating-other-user-rating"}).find("span").text
        except (AttributeError, ValueError):
            rating = "0"


        # Extract Content
        content = element.find("div", {"class": "text show-more__control"}).text

        # Extract date
        date = element.find("span", {"class": "review-date"}).text

        review = Review(review_id, user_id, movie_id, title, rating, content, date)
        datastore_object.insert_into_reviews(review)
        datastore_object.commit()

        
    except Exception as e:
        print(f"Error while extracting review (id --> {review_id}) [ERROR] {e}")
        

# Function to extract details of all reviews of a movie
def extract_movie_reviews(soup: BeautifulSoup, review_count: int, movie_id: str) -> List[Optional[Review]]:
    try:
        review_div_list = soup.find_all("div", {"class": "lister-item-content"})
        if len(review_div_list) < review_count:
            # handle dynamic Javascript here
            # Will update this in future, The given assignment asked for 10 reviews list of each movie
            # which did not require any dynamic javascript rendering as of now
            pass

        review_list = []
        for i in range(min(len(review_div_list), review_count)):
            try:
                extract_review_details(review_div_list[i], movie_id)
            except Exception as e:
                print(e)

        return review_list
    except Exception as e:
        raise Exception(f"Error extracting reviews: [ERROR] {e}")


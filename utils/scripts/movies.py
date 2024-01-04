from utils.utils import *
from scripts.reviews import *
from db import *
import re
from typing import List
from bs4 import BeautifulSoup



# Function to extract details of one movie
def extract_movie_details(soup: BeautifulSoup, movie_id: str, rank: int, movie_count: int, review_count: int, base_url: str) -> Movie:

    try:
        # Extract name
        name = soup.find("span", {"class" : "hero__primary-text"}).text

        # Extract year
        year = soup.find("ul", {"class" : "ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"}).contents[0].contents[0].text

        # Extract plot
        plot = soup.find("span", {"data-testid" : "plot-xl"}).text
        
        # Extract genre
        genre = [genre.contents[0].text for genre in soup.find_all("a", {"class" : "ipc-chip ipc-chip--on-baseAlt"})]
        
        div = soup.find("div", {"class" : "sc-69e49b85-3 dIOekc"}).contents[0].contents[0]

        # Extract cast
        cast = [cast.contents[0].text for cast in div.contents[2].contents[1].contents[0]]
        
        # Extract director
        director = [director.contents[0].text for director in div.contents[0].contents[1].contents[0]]

        # Extract writers
        writers = [writer.contents[0].text for writer in div.contents[1].contents[1].contents[0]]

        # Extract reviews
        try:
            url = base_url + f"/title/{movie_id}/reviews?sort=submissionDate&dir=desc&ratingFilter=0"
            review_soup = generate_soup(url)
            reviews = extract_movie_reviews(review_soup, review_count)
        except:
            print(f"No reviews found for movie {name} (id --> {movie_id})")
            reviews = []

        return Movie(movie_id, name, year, rank, plot, genre, cast, director, writers, reviews)
    
    except Exception as e:
        raise Exception(f"error while extracting movie (id --> {movie_id}) [ERROR]: {e}")



# Function to extract movies list based on genre
def extract_movies_list_by_genre(genre: str, base_url: str, movie_count: int, review_count: int) -> List[Movie]:
    try:
        url = base_url + f"/search/title/?title_type=feature&genres={genre}&sort=user_rating,desc&groups=top_1000"
        soup = generate_soup(url)
        movie_links = [base_url + link.get("href") for link in soup.find_all("a", {"class":"ipc-title-link-wrapper"})]
        movies = []
        if len(movie_links) <  movie_count:
            # handle dynamic Javascript here
            pass
        
        for i in range(min(len(movie_links),movie_count)):
            try:
                soup = generate_soup(movie_links[i])
                movie_id = re.search(r'/title/(.*?)/', movie_links[i]).group(1)
                movie = extract_movie_details(soup, movie_id, i + 1, movie_count, review_count, base_url)
                movies.append(movie)
            except Exception as e:
                print(f"[ERROR]: {e}")
    
        return movies
    except Exception as e:
        print(f"Error Extracting movie Links. Soup Error [ERROR]: {e}")

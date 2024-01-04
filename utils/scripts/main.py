import re
from utils.utils import *
from scripts.movies import *
from bs4 import BeautifulSoup
from typing import List

base_url = "https://www.imdb.com"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
movie_count = 20
review_count = 10

# Function to scrape genres from IMDB
def get_genres(soup: BeautifulSoup) -> List[str]:
    try:
        genres = [genre.text.strip() for genre in soup.select('#accordion-item-genreAccordion > div > section > button')]
        return genres
    except Exception as e:
        raise Exception(f"Failed to Extract genres [ERROR]: {e}")

def main():

    # Extarcting all genres firstly
    url = base_url + "/search/title"
    soup = generate_soup(url)
    genres = get_genres(soup)

    movies = {}

    for genre in genres:
        movies[genre] = extract_movies_list_by_genre(genre, base_url, movie_count, review_count)
        print(genre)
    

    print(movies)
    return 0

if __name__ == "__main__":
    main()
from utils.utils import *
from scripts.movies import *
from db import *
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

    try:
        # Extarcting all genres firstly
        url = base_url + "/search/title"
        soup = generate_soup(url)
        genres = get_genres(soup)
        datastore_object = DataStore()
        for genreName in genres:
            genre = Genre(genreName)
            datastore_object.insert_into_genres(genre)
        
        datastore_object.commit()
        movies = {}
        
        for genre in genres:
            movies[genre] = extract_movies_list_by_genre(genre, base_url, movie_count, review_count)
            print(f"Successfully extracted all movies of genre {genre}")
            
        print("Succes!!")
        return 0

    except Exception as e:
        print(f"Main Function error [ERROR]: {e}")


if __name__ == "__main__":
    main()
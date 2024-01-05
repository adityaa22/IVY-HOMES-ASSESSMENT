from utils.utils import *
from scripts.movies import *
from db import *
from bs4 import BeautifulSoup
from typing import List
import numpy as np
import concurrent.futures
from typing import List



base_url = "https://www.imdb.com"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
movie_count = 20
review_count = 10
max_workers = 8

# Function to scrape genres from IMDB
def get_genres(soup: BeautifulSoup) -> List[str]:
    try:
        genres = [genre.text.strip() for genre in soup.select('#accordion-item-genreAccordion > div > section > button')]
        return genres
    except Exception as e:
        raise Exception(f"Failed to Extract genres [ERROR]: {e}")
    
def extract_details_in_parallel(genres: List[str], base_url: str, movie_count: int, review_count: int):
    try:
        def extract_movies_for_genres(genre_list):
            result = {}
            for genre in genre_list:
                try:
                    result[genre] = extract_movies_list_by_genre(genre, base_url, movie_count, review_count)
                    print(f"Successfully extracted all movies of genre {genre}")
                except Exception as e:
                    print(f"Error extracting movies for genre {genre}: {e}")
                    result[genre] = []
            return result
        
        movies = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            # Split genres into almost equal parts for each thread
            num_threads = min(len(genres), max_workers)
            genre_parts = np.array_split(genres, num_threads)
            genre_parts = [genre_part.tolist() for genre_part in genre_parts]

            # Submit threads to extract movie lists
            futures = [executor.submit(extract_movies_for_genres, genre_part) for genre_part in genre_parts]

            # Retrieve results from completed threads
            for future in concurrent.futures.as_completed(futures):
                genre_movies = future.result()
                movies.update(genre_movies)
            
            return movies
    except Exception as e:
        raise Exception(f"Threading error [ERROR] {e}")

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
        
        movies = extract_details_in_parallel(genres, base_url, movie_count, review_count)
            
        print(movies)
        return 0

    except Exception as e:
        raise Exception(f"Main Function error [ERROR]: {e}")


if __name__ == "__main__":
    main()
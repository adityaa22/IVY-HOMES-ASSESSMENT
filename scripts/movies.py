from utils.utils import *
from scripts.reviews import *
from db import *
import re
from typing import List
from bs4 import BeautifulSoup



# Function to extract details of one movie
def extract_movie_details(soup: BeautifulSoup, movie_id: str, movie_count: int, review_count: int, base_url: str) -> Movie:

    try:

        datastore_object = DataStore()

        # Extract name
        name = soup.find("span", {"class" : "hero__primary-text"}).text

        # Extract year
        year = soup.find("ul", {"class" : "ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"}).contents[0].contents[0].text

        # Extract plot
        plot = soup.find("span", {"data-testid" : "plot-xl"}).text

        movie = Movie(movie_id, name, year, plot)
        datastore_object.insert_into_movies(movie)

        datastore_object.commit()
        
        # Extract genre
        genres = [genre.contents[0].text for genre in soup.find_all("a", {"class" : "ipc-chip ipc-chip--on-baseAlt"})]
        for genreName in genres:
            genre = datastore_object.session.query(Genre).filter_by(genre=genreName).first()
            datastore_object.insert_into_movie_genre_association(movie_id, genre)
            datastore_object.commit()
        
        div = soup.find("div", {"class" : "sc-69e49b85-3 dIOekc"}).contents[0].contents[0]

        # Extract cast
        cast_id_links = [cast_id_link.contents[0].get("href") for cast_id_link in div.contents[2].contents[1].contents[0]]
        cast_id = []
        for link in cast_id_links:
            id = re.search(r'/name/(.*?)/', link).group(1)
            cast_id.append(id)

        cast_name = [director.contents[0].text for director in div.contents[2].contents[1].contents[0]]
        for i in range (len(cast_name)):
            star = Star(cast_id[i], cast_name[i])
            datastore_object.insert_into_stars(star)
            datastore_object.commit()
            
        

        for i in range (len(cast_name)):
            star = datastore_object.session.query(Star).filter_by(id=cast_id[i]).first()
            datastore_object.insert_into_movie_star_association(movie_id, star)
            datastore_object.commit()

        
        # Extract director
        director_id_links = [director_id_link.contents[0].get("href") for director_id_link in div.contents[0].contents[1].contents[0]]
        director_id = []
        for link in director_id_links:
            id = re.search(r'/name/(.*?)/', link).group(1)
            director_id.append(id)

        director_name = [director.contents[0].text for director in div.contents[0].contents[1].contents[0]]
        for i in range (len(director_name)):
            director = Director(director_id[i], director_name[i])
            datastore_object.insert_into_directors(director)
            datastore_object.commit()



        for i in range (len(director_name)):
            director = datastore_object.session.query(Director).filter_by(id=director_id[i]).first()
            datastore_object.insert_into_movie_director_association(movie_id, director)
            datastore_object.commit()


        # Extract reviews
        try:
            url = base_url + f"/title/{movie_id}/reviews?sort=submissionDate&dir=desc&ratingFilter=0"
            review_soup = generate_soup(url)
            reviews = extract_movie_reviews(review_soup, review_count, movie_id)
        except:
            print(f"No reviews found for movie {name} (id --> {movie_id})")

        return movie
    
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
            # Will update this in future, The given assignment asked for 20 movies list of each genre
            # which did not require any dynamic javascript rendering as of now
            pass
        
        for i in range(min(len(movie_links),movie_count)):
            try:
                soup = generate_soup(movie_links[i])
                movie_id = re.search(r'/title/(.*?)/', movie_links[i]).group(1)
                movie = extract_movie_details(soup, movie_id, movie_count, review_count, base_url)
                movies.append(movie)
            except Exception as e:
                print(f"[ERROR]: {e}")
    
        return movies
    except Exception as e:
        print(f"Error Extracting movie Links. Soup Error [ERROR]: {e}")


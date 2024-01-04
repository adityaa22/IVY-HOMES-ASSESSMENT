from typing import List
from datetime import datetime
import sqlite3

class Genre:
    def __init__(self, id: str, genre: str):
        self.id = id
        self.genre = genre

class Director:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Writer:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Star:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name



class Review:
    def __init__(self, review_id: str, user: str, title: str, rating: str, content: str, date: datetime):
        self.review_id = review_id
        self.user = user
        self.title = title
        self.rating = rating
        self.content = content
        self.date = date

class Movie:
    def __init__(self, movie_id: str, name: str, year: str, rank: int, plot: str, genre: List[str], cast: List[str], 
                 director: List[str], writers: List[str], reviews: List[Review]):
        self.movie_id = movie_id
        self.name = name
        self.year = year
        self.rank = rank
        self.plot = plot
        self.genre = genre
        self.cast = cast
        self.director = director
        self.writers = writers
        self.reviews = reviews

class DataStore:
    def __init__(self):
        self.conn = sqlite3.connect('imdb.db')
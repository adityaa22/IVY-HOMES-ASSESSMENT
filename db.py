import os
from sqlalchemy import (
    ForeignKey, 
    create_engine, 
    Column, 
    Integer, 
    String, 
    Table
)
from sqlalchemy.orm import(
    relationship,
    declarative_base, 
    sessionmaker
)

connection_str = "sqlite:///imdb.db"
engine = create_engine(connection_str)
Base = declarative_base()
CUR_DIR = os.getcwd()
db_path = CUR_DIR + "imdb.db"

# Association Tables
movie_genre_association_table = Table(
    'movie_genre_association',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre', ForeignKey('genres.genre'))
)

movie_director_association_table = Table(
    'movie_director_association',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('director_id', ForeignKey('directors.id'))
)

movie_star_association_table = Table(
    'movie_star_association',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('star_id', ForeignKey('stars.id'))
)


# Models

class Genre(Base):
    __tablename__ = 'genres'
    genre = Column(String(), primary_key=True, nullable=False)

    def __init__(self, genre: str):
        self.genre = genre
    
    def __repr__(self):
        return f"<Genre= {self.genre}>"
    

class Director(Base):
    __tablename__ = 'directors'
    id = Column(String(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False)
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"<Name= {self.name}>"

class Star(Base):
    __tablename__ = 'stars'
    id = Column(String(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False)
 

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"<Name= {self.name}>"

class User(Base):
    __tablename__ = 'users'
    id = Column(String(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False)

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f"<Name= {self.name}>"

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String(), primary_key=True, nullable=False)
    user_id = Column(String(), ForeignKey("users.id"))
    movie_id = Column(String(), ForeignKey("movies.id"))
    title = Column(String(), nullable=False)
    rating = Column(String(), nullable=False)
    content = Column(String(), nullable=False)
    date = Column(String(), nullable=False)

    def __init__(self, id: str, user_id: str, movie_id: str, title: str, rating: str, content: str, date: str):
        self.id = id
        self.user_id = user_id
        self.movie_id = movie_id
        self.title = title
        self.rating = rating
        self.content = content
        self.date = date

    def __repr__(self):
        return f"<Title= {self.title}> <Rating= {self.rating}> <Content= {self.content}> <Date= {self.date}>"

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(String(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False)
    year = Column(String(), nullable=False)
    rank = Column(Integer(), nullable=False)
    plot = Column(String(), nullable=False)
    genres = relationship('Genre', secondary=movie_genre_association_table, backref='genre_ref')
    directors = relationship('Director', secondary=movie_director_association_table, backref='director_ref')
    stars = relationship('Star', secondary=movie_star_association_table, backref='star_ref')
    

    def __init__(self, id: str, name: str, year: str, rank: int, plot: str):
        self.id = id
        self.name = name
        self.year = year
        self.rank = rank
        self.plot = plot

    def __repr__(self):
        return f"<Name= {self.name}> <Year= {self.year}> <Rank= {self.rank}> <Plot= {self.plot}>"

class DataStore:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStore, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.session = sessionmaker()(bind=engine, expire_on_commit=False)
        if os.path.exists(db_path):
            pass
        else:
            Base.metadata.create_all(engine)
    
    def insert_into_genres(self, genre: Genre)-> None:
        try:
            exists = bool(self.session.query(Genre).filter_by(genre=genre.genre).first())
            if exists:
                pass
            else:
                self.session.add(genre)

        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")

        
    def insert_into_reviews(self, review: Review)-> None:
        try:
            exists = bool(self.session.query(Review).filter_by(id=review.id).first())
            if exists:
                pass
            else:
                self.session.add(review)
        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")
        
    def insert_into_movies(self, movie: Movie)-> None:
        try:
            exists = bool(self.session.query(Movie).filter_by(id=movie.id).first())
            if exists:
                pass
            else:
                self.session.add(movie)
        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")
        
    def insert_into_directors(self, director: Director)-> None:
        try:
            exists = bool(self.session.query(Director).filter_by(id=director.id).first())
            if exists:
                pass
            else:
                self.session.add(director)
        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")
        
    def insert_into_stars(self, star: Star)-> None:
        try:
            exists = bool(self.session.query(Star).filter_by(id=star.id).first())
            if exists:
                pass
            else:
                self.session.add(star)
        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")
        
    def insert_into_users(self, user: User)-> None:
        try:
            exists = bool(self.session.query(User).filter_by(id=user.id).first())
            if exists:
                pass
            else:
                self.session.add(user)
        except Exception as e:
            raise Exception(f"Failed to add data [ERROR]: {e}")
        
    def insert_into_movie_genre_association(self, movie_id: str, genre: Genre)->None:
        try:
            movie = self.session.query(Movie).filter_by(id = movie_id).first()
            movie.genres.append(genre)
        except Exception as e:
            print(f"insert_into_movie_genre_association failed [ERROR]: {e}")

    def insert_into_movie_director_association(self, movie_id: str, director: Director)->None:
        try:
            movie = self.session.query(Movie).filter_by(id = movie_id).first()
            movie.directors.append(director)
        except Exception as e:
            print(f"insert_into_movie_director_association failed [ERROR]: {e}")

    def insert_into_movie_star_association(self, movie_id: str, star: Star)->None:
        try:
            movie = self.session.query(Movie).filter_by(id = movie_id).first()
            movie.stars.append(star)
        except Exception as e:
            print(f"insert_into_movie_star_association failed [ERROR]: {e}")

    def commit(self):
        self.session.commit()
    



import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(15), nullable = True)
    occupation = Column(String(15), nullable = True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    movie_name = Column(String(64), nullable = True)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(64), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, nullable = True)
    user_id = Column(Integer, nullable = True)
    rating = Column(Integer, nullable = True)
    timestamp = Column(Integer, nullable = True)


def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def create_tables():
    engine = create_engine("sqlite:///ratings.db", echo=True)
    Base.metadata.create_all(engine)
    
### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

import datetime
import correlation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, update
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session 

# # ENGINE = None
# Session = None

ENGINE = create_engine("sqlite:///ratings.db", echo=False) 
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

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

    # also has ratings attribute

    def similarity(self,other):
        u_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        other_users = [ r.user for r in other_ratings ]
        similarities = [ (self.similarity(other_user), other_user) \
            for other_user in other_users ]
        similarities.sort(reverse = True)
        top_user = similarities[0]
        matched_rating = None
        for rating in other_ratings:
            if rating.user_id == top_user[1].id:
                matched_rating = rating
                break
        return matched_rating.rating * top_user[0]

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    movie_name = Column(String(64), nullable = True)
    release_year = Column(DateTime, nullable = True)
    imdb_url = Column(String(64), nullable = True)

    # also has ratings attribute

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=id)) #this sets relationship between user and ratings
    movie = relationship("Movie", backref=backref("ratings", order_by=id)) #this sets relationship between movie and ratings

def create_tables():
    engine = create_engine("sqlite:///ratings.db", echo=True)
    Base.metadata.create_all(engine)


### End class declarations

def main():
    pass

if __name__ == "__main__":
    main()

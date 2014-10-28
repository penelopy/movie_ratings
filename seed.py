from datetime import datetime, date
import model
import csv

def load_users(db_session):
    f = open('seed_data/u.user','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split('|')

        newuser = model.User(id = fields[0],
                        age= fields[1],
                        gender = fields[2],
                        occupation = fields[3],
                        zipcode = fields[4])

        db_session.add(newuser)

    f.close()


def load_movies(db_session):
    f = open('seed_data/u.item','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split('|')

        datetime_obj = datetime.strptime(fields[2], "%d-%b-%Y")
        datetime_obj = datetime_obj.date()

        movie_name = fields[1]
        movie_name = movie_name.decode("latin-1").strip().split(" ")
        movie_name.pop()
        movie_name = (" ").join(movie_name)

        newmovie = model.Movie(id = fields[0],
                            movie_name= movie_name,
                            release_year = datetime_obj,
                            imdb_url = fields[3])

        db_session.add(newmovie)

    f.close()

def load_ratings(db_session):
    f = open('seed_data/u.data','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split()

        newRating = model.Rating(movie_id = fields[0],
                user_id = fields[1],
                rating = fields[2])

        db_session.add(newRating)

    f.close()


def main(db_session):
    # load_users(db_session)
    # load_movies(db_session)
    # load_ratings(db_session)
    # db_session.commit()

if __name__ == "__main__":
    db_session = model.connect()
    main(db_session)


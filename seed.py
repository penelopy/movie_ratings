import datetime
import model
import csv

def load_users(session):
    f = open('seed_data/u.user','r')

    lines = f.readlines()
    
    udict = {}

    for line in lines:
        fields = line.split('|')
        id = fields[0]

        udict[id] = {'age': fields[1],
                        'gender': fields[2],
                        'occupation': fields[3],
                        'zipcode': fields[4]}

    ulist = []
    for i in range(1,len(udict)):
        newuser = model.User(age= udict[str(i)]['age'],
                        gender = udict[str(i)]['gender'],
                        occupation = udict[str(i)]['occupation'],
                        zipcode = udict[str(i)]['zipcode'])

        ulist.append(newuser)
        
    for user in ulist:
        session.add(user)

    session.commit()

    f.close()


def load_movies(session):
    f = open('seed_data/u.item','r')

    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12 }

    lines = f.readlines()
    
    mdict = {}

    for line in lines:
        fields = line.split('|')
        id = fields[0]

        # Converting date strings to Python datetime format
        date = fields[2].split('-')
        print date
        if len(date) == 3:
            date[1] = month_dict.get(date[1],0)
            date_obj = datetime.date(int(date[2]),int(date[1]),int(date[0]))
        else: # if there is no date, put in default value
            date_obj = (0,0,0)

        # Getting key error for id 1
        mdict[id] = {'movie_name': fields[1],
                    'release_date': date_obj,
                    'imdb_url': fields[3]}

    mlist = []
    for i in range(1,len(mdict)):
        newmovie = model.Movie(movie_name= mdict[i]['movie_name'],
                        released_at = date_obj,
                        imdb_url = mdict[i]['imdb_url'])

        mlist.append(newmovie)
        
    for movie in mlist:
        session.add(movie)

    session.commit()
    f.close()

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    # load_users(s)
    load_movies(s)

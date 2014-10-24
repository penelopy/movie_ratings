from datetime import datetime, date
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

    lines = f.readlines()
    
    mdict = {}

    for line in lines:
        fields = line.split('|')
        id = fields[0]

        # 01-Jan-1995

        datetime_obj = datetime.strptime(fields[2], "%d-%b-%Y")
        datetime_obj = datetime_obj.date()

        movie_name = fields[1]
        movie_name = movie_name.decode("latin-1").strip().split(" ")
        movie_name.pop()
        movie_name = (" ").join(movie_name)
 
        mdict[id] = {'movie_name': fields[1],
                    'release_date': datetime_obj,
                    'imdb_url': fields[3]}


    mlist = []
    for i in range(1,len(mdict)):
        i = str(i)
        if i in mdict:
            newmovie = model.Movie(movie_name= movie_name,
                            released_at = datetime_obj,
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
    s = model.connect()
    # load_users(s)
    load_movies(s)

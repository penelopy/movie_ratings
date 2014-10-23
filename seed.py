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


def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    load_users(s)

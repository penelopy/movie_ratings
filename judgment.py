from flask import Flask, render_template, redirect, request
from flask import session as flask_session
import model

app = Flask(__name__)

app.secret_key = 'a4c96d59-57a8-11e4-8b97-80e6500ee2f6'

@app.route("/")
def index():
    return render_template("user_signup.html")


@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).first()

    if user:
        flask_session['user'] = [user.id, user.email]
        print "Login successful."           # Flash message
    else:
        print "Username/password is invalid"
        
    return redirect("/userlist")


@app.route('/userlist')
def user_list(): 
    user_list = model.session.query(model.User).limit(15).all()
    return render_template("user_list.html", users=user_list)

@app.route('/user')
def user_reviews():
    user_id = request.args.get("user")
    user = model.session.query(model.User).get(user_id) # User
    user_rating_dict = {}

    for rating in user.ratings:
        movie = model.session.query(model.Movie).get(rating.movie_id)
        user_rating_dict[rating.movie_id] = [movie.movie_name, rating.rating, rating.movie_id]

    return render_template("user_rating.html", reviews=user_rating_dict, user=user.id)

@app.route('/movie')
def movie_reviews():
    movie_id = request.args.get("movie")
    movie = model.session.query(model.Movie).get(movie_id) # Movie
    movie_rating_dict = {}

    for rating in movie.ratings:
        user = model.session.query(model.User).get(rating.user_id) # User
        movie_rating_dict[user.id] = rating.rating

    return render_template("movie_ratings.html", reviews=movie_rating_dict, movie=movie)

@app.route('/new_review', methods=['POST'])
def add_review():
    movie_id = request.args.get("movie")
    user_id = flask_session['user'][0]
    rating = request.form['rating']

    new_review = model.Rating(movie_id = movie_id, 
                    user_id = user_id, 
                    rating = rating)
    model.session.add(new_review)
    model.session.commit()

    url = '/movie?movie=' + movie_id
    return redirect(url)

@app.route("/newuser", methods=['POST'])
def add_new_user():

    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']
    gender = request.form['gender']
    occupation = request.form['occupation']

    new_user = model.User(email = email, 
                    password = password, 
                    age = age, 
                    gender = gender, 
                    occupation = occupation, 
                    zipcode = zipcode)
    
    model.session.add(new_user)                  
    model.session.commit()

    return render_template("user_signup_success.html", user = new_user)

if __name__ == "__main__":
    app.run(debug = True)

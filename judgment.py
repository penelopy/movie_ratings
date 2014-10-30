from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model

app = Flask(__name__)

app.secret_key = 'a4c96d59-57a8-11e4-8b97-80e6500ee2f6'

@app.before_request
def check_login():
    user_data = flask_session.get('user')
    if user_data and len(user_data) > 1:
        g.user_id = user_data[0]
        g.user_email = user_data[1]

@app.route("/")
def index():
    # Replace with cover page later
    user_list = model.session.query(model.User).limit(15).all()
    return render_template("user_list.html", users=user_list)

@app.route('/signin')
def signin():
    return render_template("user_login.html")


@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).first()

    if user:
        flask_session['user'] = [user.id, user.email]
        flash("Login successful.")
        # url = "/user?user=" + str(user.id) ## Do away with this and use route below
        return redirect(url_for('user_reviews', user_id=user.id))         
    else:
        flash("Username/password is invalid")
        return redirect(url_for('index'))

@app.route("/logout", methods=['GET','POST'])
def logout():
    flask_session['user'] = []
    flash("You are logged out.")
    return redirect(url_for('index'))

# @app.route()
    ## Make a page and route that goes to the current user's ratings / account info
    

# HTML
# <a href="/movie/{{movie.id}}">link</a>
# evaluates to <a href="/movie/4">link</a>"

# @app.route("/movie/<int:id>")
# def route_name(id):
#     request.args.get("id")
#     do some stuff


@app.route('/user/<int:user_id>')
def user_reviews(user_id):
    # user_id = request.args.get("id")
    user = model.session.query(model.User).get(user_id) # User
    user_rating_dict = {}

    for rating in user.ratings:
        movie_rating = rating.rating
        movie_name = rating.movie.movie_name
        movie_id = rating.movie.id
        user_rating_dict[rating.movie_id] = [movie_name, movie_rating, movie_id]

    return render_template("user_rating.html", reviews=user_rating_dict, user=user.id)

@app.route('/movie/<int:movie_id>')
def movie_reviews(movie_id):
    # movie_id = request.args.get("id")
    # movie_id = int(movie_id)
    movie = model.session.query(model.Movie).get(movie_id) # Movie    
    movie_rating_dict = {}

    for rating in movie.ratings:               
        movie_rating = rating.rating
        user_id = rating.user_id 
        movie_rating_dict[user_id] = movie_rating

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

    url = '/movie?movie=' + movie_rating_dict   # Need to redo this url
    return redirect(url)


@app.route('/update_review/<int:movie_id>', methods=['GET','POST'])
def update_review(movie_id):
    # receive rating
    # and set new new rating
    # return new rating

    # user_id.rating = new_rating
    m = movie_id
    u = flask_session['user'][0]
    r = request.form['rating']

    model.Rating.update().values(rating=r).where(user_id = u).where(movie_id=m)                 
    model.session.commit()
    flash("Review updated.")
    return redirect("/myaccount")

@app.route('/myaccount')
def account_page():
    user_id = flask_session['user'][0]
    user = model.session.query(model.User).get(user_id) # User
    user_rating_dict = {}

    for rating in user.ratings:
        movie_rating = rating.rating
        movie_name = rating.movie.movie_name
        movie_id = rating.movie.id
        user_rating_dict[rating.movie_id] = [movie_name, movie_rating, movie_id]

    return render_template("your_ratings_page.html",reviews=user_rating_dict, user=user.id )

@app.route("/registration")
def registration_form():
    return render_template("registration_form.html")


@app.route("/newuser", methods=['POST'])
def add_new_user():

    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']
    gender = request.form['gender']
    occupation = request.form['occupation']

    new_user = model.User(email = email, 
                    password = password,    # Need to encrypt the password
                    age = age, 
                    gender = gender, 
                    occupation = occupation, 
                    zipcode = zipcode)
    
    model.session.add(new_user)                  
    model.session.commit()

    return render_template("user_signup_success.html", user = new_user)

if __name__ == "__main__":
    app.run(debug = True)

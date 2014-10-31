from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model

app = Flask(__name__)

app.secret_key = 'a4c96d59-57a8-11e4-8b97-80e6500ee2f6'

#Run when browser is refreshed and sets g for id and email of the user that is logged in
@app.before_request
def check_login():
    user_data = flask_session.get('user') 
    if user_data and len(user_data) > 1:
        g.user_id = user_data[0]
        g.user_email = user_data[1]

#Home page view. Queries database for 15 users and displays the number of ratings they have done
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
    #A Database query that looks in the User table for the email and password and it return the user object/instance
    user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).one()

    if user:
        flask_session['user'] = [user.id, user.email] #adds the current user to the flask session
        flash("Login successful.")
        return redirect(url_for('user_reviews', user_id=user.id))         
    else:
        flash("Username/password is invalid")
        return redirect(url_for('index'))

@app.route("/logout", methods=['GET','POST'])
def logout():
    flask_session['user'] = [] #clears the user key stored in the flask session
    flash("You are logged out.")
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>')
def user_reviews(user_id):
    #Queries the User table by user_id and returns a user object/instance
    user_obj = model.session.query(model.User).get(user_id) # User
    return render_template("user_rating.html", ratings=user_obj.ratings, user=user_obj.id)

@app.route('/movie/<int:movie_id>')
def movie_reviews(movie_id):
    movie_obj = model.session.query(model.Movie).get(movie_id) # Movie    
    return render_template("movie_ratings.html", movie=movie_obj)

@app.route('/new_review/<int:movie_id>', methods=['POST'])
def add_review(movie_id):
    user_id = flask_session['user'][0]
    rating = request.form['rating']

    new_review = model.Rating(movie_id = movie_id, 
                    user_id = user_id, 
                    rating = rating)
    model.session.add(new_review)
    model.session.commit()

    return redirect(url_for('account_page'))


@app.route('/update_review/<int:movie_id>', methods=['GET','POST'])
def update_review(movie_id):
    m = movie_id
    u = flask_session['user'][0]
    r = request.form.get('rating')

    rating_obj = model.session.query(model.Rating).filter_by(user_id = u).filter_by(movie_id = m).one()                
    rating_obj.rating = r #changes the old rating from the database to the new rating -"r"
    model.session.commit()
    flash("Review updated.")
    return redirect("/myaccount")

@app.route('/myaccount')
def account_page():
    user_id = flask_session['user'][0]
    user_obj = model.session.query(model.User).get(user_id) # User
    return render_template("your_ratings_page.html", ratings=user_obj.ratings, user=user_obj.id)

@app.route("/registration")
def registration_form():
    return render_template("registration_form.html")


@app.route("/newuser", methods=['POST'])
def add_new_user():
    #request.form takes the information submitted in the form on registration.html
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
